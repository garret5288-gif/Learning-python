"""
Automated reporting and alerts

Scans the file upload directory, summarizes processed results, and sends
simulated email/SMS notifications using the notification module.

Run:
  python3 week14/day4/automated_reporting.py \
	  --uploads-dir week14/day4/uploads \
	  --email user@example.com \
	  --phone +15551234567
"""

from __future__ import annotations

import argparse
import os
from typing import List, Dict, Any

try:
	# Prefer using the existing processor from the upload app
	from file_upload import process_file  # type: ignore
except Exception:
	process_file = None  # type: ignore

from notification import NotificationManager, EmailNotifier, SMSNotifier


ALLOWED = {".csv", ".json", ".txt"}


def simple_process_file(path: str) -> Dict[str, Any]:
	"""Fallback processor used if file_upload.process_file isn't importable."""
	name = os.path.basename(path)
	_, ext = os.path.splitext(name.lower())
	size = os.path.getsize(path)
	out: Dict[str, Any] = {"filename": name, "type": ext, "size": size}
	try:
		with open(path, "r", encoding="utf-8", errors="ignore") as f:
			content = f.read()
		if ext == ".txt":
			out["lines"] = content.count("\n") + (1 if content else 0)
			out["preview"] = content[:200]
		elif ext == ".json":
			import json

			try:
				obj = json.loads(content)
				out["json_type"] = type(obj).__name__
			except Exception as e:  # noqa: BLE001
				out["error"] = f"Invalid JSON: {e}"
		elif ext == ".csv":
			import csv, io

			rows = list(csv.DictReader(io.StringIO(content)))
			out["rows"] = len(rows)
		else:
			out["preview"] = content[:200]
	except Exception as e:  # noqa: BLE001
		out["error"] = str(e)
	return out


def scan_and_summarize(uploads_dir: str) -> List[Dict[str, Any]]:
	results: List[Dict[str, Any]] = []
	if not os.path.isdir(uploads_dir):
		return results
	for name in sorted(os.listdir(uploads_dir)):
		_, ext = os.path.splitext(name.lower())
		if ext not in ALLOWED:
			continue
		path = os.path.join(uploads_dir, name)
		if not os.path.isfile(path):
			continue
		if process_file:
			try:
				results.append(process_file(path))  # type: ignore[misc]
			except Exception:  # noqa: BLE001
				results.append(simple_process_file(path))
		else:
			results.append(simple_process_file(path))
	return results


def build_report(results: List[Dict[str, Any]]) -> str:
	lines = ["Upload Report", "================"]
	if not results:
		lines.append("No files found.")
		return "\n".join(lines)
	for r in results:
		lines.append(f"- {r.get('filename')} ({r.get('type')}, {r.get('size','?')} bytes)")
		if "error" in r:
			lines.append(f"  ERROR: {r['error']}")
		if r.get("type") == ".csv" and "rows" in r:
			lines.append(f"  Rows: {r['rows']}")
		if r.get("type") == ".json" and r.get("json_type"):
			lines.append(f"  JSON type: {r['json_type']}")
		if r.get("type") == ".txt" and r.get("lines") is not None:
			lines.append(f"  Lines: {r['lines']}")
	return "\n".join(lines)


def detect_alerts(results: List[Dict[str, Any]], csv_min_rows: int) -> List[str]:
	alerts: List[str] = []
	for r in results:
		if r.get("error"):
			alerts.append(f"Error in {r.get('filename')}: {r['error']}")
		if r.get("type") == ".csv" and r.get("rows") is not None and int(r["rows"]) < csv_min_rows:
			alerts.append(f"CSV {r.get('filename')} has only {r['rows']} rows (< {csv_min_rows})")
	return alerts


def main():
	ap = argparse.ArgumentParser(description="Automate reporting and alerts for uploaded files")
	ap.add_argument("--uploads-dir", default=os.path.join(os.path.dirname(__file__), "uploads"))
	ap.add_argument("--email")
	ap.add_argument("--phone")
	ap.add_argument("--csv-min-rows", type=int, default=1, help="Alert if CSV rows < this value")
	args = ap.parse_args()

	results = scan_and_summarize(args.uploads_dir)
	report = build_report(results)
	alerts = detect_alerts(results, csv_min_rows=args.csv_min_rows)

	subject = f"Upload Report ({len(results)} files)"
	sms_summary = f"Files: {len(results)}; Alerts: {len(alerts)}"

	# Print to console always
	print(report)
	if alerts:
		print("\nALERTS:")
		for a in alerts:
			print("-", a)

	# Notify if destinations provided
	notifier = NotificationManager(EmailNotifier(), SMSNotifier())
	if args.email:
		notifier.send_email(args.email, subject=subject, body=report + ("\n\nALERTS:\n" + "\n".join(alerts) if alerts else ""))
	if args.phone:
		# keep SMS short
		sms_body = sms_summary
		if alerts:
			sms_body += ": " + "; ".join(alerts[:3])
		notifier.send_sms(args.phone, body=sms_body)


if __name__ == "__main__":
	main()

