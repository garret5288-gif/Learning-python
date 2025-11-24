import argparse
import json
import os
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple


def connect(db_path: str) -> sqlite3.Connection:
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
	return conn


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
	cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
	return cur.fetchone() is not None


def get_columns(conn: sqlite3.Connection, table: str) -> Dict[str, Dict[str, Any]]:
	cols: Dict[str, Dict[str, Any]] = {}
	for row in conn.execute(f"PRAGMA table_info({table})"):
		cols[row[1]] = {
			"cid": row[0],
			"name": row[1],
			"type": row[2],
			"notnull": bool(row[3]),
			"dflt_value": row[4],
			"pk": bool(row[5]),
		}
	return cols


def run_row_count(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table = t["table"]
	where = t.get("where")
	op = t.get("op", "=")
	value = t.get("value")
	if value is None:
		return False, "row_count requires 'value'"
	sql = f"SELECT COUNT(*) as c FROM {table}"
	if where:
		sql += f" WHERE {where}"
	c = conn.execute(sql).fetchone()[0]
	ops = {
		"=": c == value,
		"==": c == value,
		"!=": c != value,
		">": c > value,
		">=": c >= value,
		"<": c < value,
		"<=": c <= value,
	}
	ok = ops.get(op)
	if ok is None:
		return False, f"unsupported op: {op}"
	return bool(ok), f"count {c} {op} {value}"


def run_not_null(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table, column = t["table"], t["column"]
	where = t.get("where")
	sql = f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL"
	if where:
		sql += f" AND ({where})"
	c = conn.execute(sql).fetchone()[0]
	return c == 0, f"NULL count in {table}.{column} = {c}"


def run_unique(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table = t["table"]
	columns: Sequence[str] = t["columns"]
	cols = ", ".join(columns)
	sql = (
		f"SELECT {cols}, COUNT(*) c FROM {table} "
		f"GROUP BY {cols} HAVING c > 1 LIMIT 1"
	)
	row = conn.execute(sql).fetchone()
	return row is None, "no duplicates" if row is None else f"duplicate found: {dict(row)}"


def run_value_range(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table, column = t["table"], t["column"]
	min_v = t.get("min")
	max_v = t.get("max")
	inclusive = bool(t.get("inclusive", True))
	clauses = [f"{column} IS NOT NULL"]
	if min_v is not None:
		clauses.append(f"{column} {'>=' if inclusive else '>'} {min_v}")
	if max_v is not None:
		clauses.append(f"{column} {'<=' if inclusive else '<'} {max_v}")
	where_ok = " AND ".join(clauses)
	sql_bad = f"SELECT COUNT(*) FROM {table} WHERE NOT ({where_ok})"
	bad = conn.execute(sql_bad).fetchone()[0]
	msg = f"out_of_range={bad}"
	return bad == 0, msg


def run_in_set(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table, column = t["table"], t["column"]
	allowed: Sequence[Any] = t["allowed"]
	ignore_nulls = bool(t.get("ignore_nulls", True))
	allowed_list = ",".join([repr(v) for v in allowed])
	conds = [f"{column} NOT IN ({allowed_list})"]
	if ignore_nulls:
		conds.append(f"{column} IS NOT NULL")
	where = " AND ".join(conds)
	sql = f"SELECT COUNT(*) FROM {table} WHERE {where}"
	bad = conn.execute(sql).fetchone()[0]
	return bad == 0, f"invalid_values={bad}"


def run_foreign_key(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table, column = t["table"], t["column"]
	ref_table, ref_column = t["ref_table"], t.get("ref_column", "id")
	sql = (
		f"SELECT COUNT(*) FROM {table} AS a "
		f"LEFT JOIN {ref_table} AS b ON a.{column} = b.{ref_column} "
		f"WHERE a.{column} IS NOT NULL AND b.{ref_column} IS NULL"
	)
	bad = conn.execute(sql).fetchone()[0]
	return bad == 0, f"orphans={bad}"


def run_column_exists(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table, column = t["table"], t["column"]
	cols = get_columns(conn, table)
	if column not in cols:
		return False, f"column {column} missing"
	exp_type = t.get("type")
	if exp_type:
		actual = (cols[column]["type"] or "").upper()
		if actual != exp_type.upper():
			return False, f"type {actual} != {exp_type}"
	return True, "ok"


def run_table_exists(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	table = t["table"]
	ok = table_exists(conn, table)
	return ok, ("exists" if ok else "missing")


def run_query_expect(conn: sqlite3.Connection, t: Dict[str, Any]) -> Tuple[bool, str]:
	sql = t["sql"]
	op = t.get("op", "=")
	value = t.get("value")
	row = conn.execute(sql).fetchone()
	if row is None:
		return False, "query returned no rows"
	# If row is Row, get first column
	result = list(row)[0] if isinstance(row, sqlite3.Row) else row[0]
	ops = {
		"=": result == value,
		"==": result == value,
		"!=": result != value,
		">": result > value,
		">=": result >= value,
		"<": result < value,
		"<=": result <= value,
	}
	ok = ops.get(op)
	if ok is None:
		return False, f"unsupported op: {op}"
	return bool(ok), f"result {result} {op} {value}"


CHECK_RUNNERS = {
	"table_exists": run_table_exists,
	"column_exists": run_column_exists,
	"row_count": run_row_count,
	"not_null": run_not_null,
	"unique": run_unique,
	"value_range": run_value_range,
	"in_set": run_in_set,
	"foreign_key": run_foreign_key,
	"query_expect": run_query_expect,
}


def list_schema(conn: sqlite3.Connection) -> Dict[str, List[str]]:
	schema: Dict[str, List[str]] = {}
	for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
		tbl = r[0]
		schema[tbl] = list(get_columns(conn, tbl).keys())
	return schema


def load_tests(path: str) -> List[Dict[str, Any]]:
	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
	if isinstance(data, dict) and "tests" in data:
		return data["tests"]
	if isinstance(data, list):
		return data
	raise ValueError("Invalid tests file format")


def run_tests(db_path: str, tests: List[Dict[str, Any]], verbose: bool = False) -> int:
	if not os.path.exists(db_path):
		print(f"DB missing: {db_path}")
		return 1
	conn = connect(db_path)
	passed = 0
	failed = 0
	for t in tests:
		name = t.get("name", f"{t.get('check')} on {t.get('table','')}" )
		check = t.get("check")
		if not check or check not in CHECK_RUNNERS:
			print(f"SKIP - {name} (unknown check: {check})")
			continue
		try:
			ok, msg = CHECK_RUNNERS[check](conn, t)
		except Exception as e:
			ok, msg = False, f"error: {e}"
		if ok:
			passed += 1
			print(f"PASS - {name} :: {msg}")
		else:
			failed += 1
			print(f"FAIL - {name} :: {msg}")
			if verbose:
				print("  Test:", json.dumps(t, ensure_ascii=False))
	print(f"\nSummary: Passed={passed} Failed={failed}")
	return 0 if failed == 0 else 2


def main(argv: Optional[Sequence[str]] = None) -> int:
	parser = argparse.ArgumentParser(description="SQLite database validation runner")
	parser.add_argument("database", nargs="?", help="Path to SQLite .db file")
	parser.add_argument("tests", nargs="?", help="Path to JSON tests file")
	parser.add_argument("--scan", action="store_true", help="List tables and columns then exit")
	parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output on failures")
	args = parser.parse_args(argv)

	if not args.database:
		print("Usage: database_test.py <database> [tests.json] [--scan] [-v]")
		return 1

	if args.scan:
		conn = connect(args.database)
		schema = list_schema(conn)
		print(f"Schema for {args.database}:")
		for tbl, cols in schema.items():
			print(f"- {tbl}: {', '.join(cols)}")
		return 0

	tests: List[Dict[str, Any]] = []
	if args.tests:
		tests = load_tests(args.tests)
	else:
		# Minimal default: ensure at least one table exists
		tests = [
			{"name": "Has at least one table", "check": "query_expect", "sql": "SELECT COUNT(*) FROM sqlite_master WHERE type='table'", "op": ">", "value": 0}
		]

	# Allow per-test database override; otherwise use provided database
	grouped: Dict[str, List[Dict[str, Any]]] = {}
	for t in tests:
		db = t.get("database", args.database)
		grouped.setdefault(db, []).append(t)

	exit_code = 0
	for db, tests_for_db in grouped.items():
		print(f"\n=== Running {len(tests_for_db)} tests on {db} ===")
		code = run_tests(db, tests_for_db, verbose=args.verbose)
		if code != 0:
			exit_code = code
	return exit_code


if __name__ == "__main__":
	sys.exit(main())

