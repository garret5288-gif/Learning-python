import sys
import json
import urllib.request
import urllib.error


def request(method, url, headers=None, data=None, timeout=10):
	headers = headers or {}
	body = None
	if data is not None:
		if isinstance(data, (dict, list)):
			body = json.dumps(data).encode("utf-8")
			headers.setdefault("Content-Type", "application/json")
		elif isinstance(data, str):
			body = data.encode("utf-8")
		else:
			body = data
	req = urllib.request.Request(url, data=body, method=method.upper(), headers=headers)
	try:
		with urllib.request.urlopen(req, timeout=timeout) as resp:
			return resp.status, dict(resp.headers), resp.read()
	except urllib.error.HTTPError as e:
		return e.code, dict(e.headers), e.read()
	except urllib.error.URLError as e:
		return None, {}, str(e).encode("utf-8")


def assert_contains(haystack: bytes, needle: str) -> bool:
	try:
		return needle.encode("utf-8") in haystack
	except Exception:
		return False


def run_test(test):
	name = test.get("name", "unnamed")
	method = test.get("method", "GET")
	url = test["url"]
	exp_status = test.get("status", 200)
	exp_json_contains = test.get("json_contains")  # dict of expected keys/values (substring/equals)
	exp_text_contains = test.get("text_contains")  # string or list of strings
	headers = test.get("headers") or {}
	data = test.get("data")

	status, resp_headers, body = request(method, url, headers, data, timeout=test.get("timeout", 10))
	ok = True
	failures = []

	if status != exp_status:
		ok = False
		failures.append(f"status={status} expected={exp_status}")

	# JSON checks
	if exp_json_contains is not None:
		try:
			payload = json.loads(body.decode("utf-8"))
			# If payload is a list, support index checks via numeric keys and simple length_at_least rule
			if isinstance(payload, list):
				for k, v in exp_json_contains.items():
					if k == "length_at_least":
						if not isinstance(v, int) or len(payload) < v:
							ok = False
							failures.append(f"json list length {len(payload)} < {v}")
						continue
					try:
						idx = int(k)
					except Exception:
						ok = False
						failures.append(f"json list invalid index key: {k}")
						continue
					if idx < 0 or idx >= len(payload):
						ok = False
						failures.append(f"json list missing index: {idx}")
						continue
					if v is None:
						continue  # presence only
					actual = payload[idx]
					if isinstance(v, dict) and isinstance(actual, dict):
						# subset match for dicts
						for subk, subv in v.items():
							if subk not in actual:
								ok = False
								failures.append(f"json[{idx}] missing key: {subk}")
								continue
							if subv is None:
								continue
							if isinstance(subv, str) and isinstance(actual[subk], str):
								if subv not in actual[subk]:
									ok = False
									failures.append(f"json[{idx}]['{subk}'] does not contain '{subv}'")
							elif actual[subk] != subv:
								ok = False
								failures.append(f"json[{idx}]['{subk}'] != {subv} (got {actual[subk]})")
					else:
						if isinstance(v, str) and isinstance(actual, str):
							if v not in actual:
								ok = False
								failures.append(f"json[{idx}] does not contain '{v}' (got '{str(actual)[:60]}...')")
						elif actual != v:
							ok = False
							failures.append(f"json[{idx}] != {v} (got {actual})")
			else:
				for k, v in exp_json_contains.items():
					if k not in payload:
						ok = False
						failures.append(f"json missing key: {k}")
						continue
					if v is None:
						continue
					actual = payload[k]
					if isinstance(v, str) and isinstance(actual, str):
						if v not in actual:
							ok = False
							failures.append(f"json[{k}] does not contain '{v}' (got '{actual[:60]}...')")
					else:
						if actual != v:
							ok = False
							failures.append(f"json[{k}] != {v} (got {actual})")
		except Exception as e:
			ok = False
			failures.append(f"invalid json: {e}")

	# Text checks
	if exp_text_contains is not None:
		needles = exp_text_contains if isinstance(exp_text_contains, list) else [exp_text_contains]
		for s in needles:
			if not assert_contains(body, s):
				ok = False
				failures.append(f"body missing text: {s}")

	return ok, {
		"name": name,
		"method": method,
		"url": url,
		"status": status,
		"failures": failures,
	}


def load_tests_from_file(path):
	try:
		with open(path, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception as e:
		print(f"Failed to load tests from {path}: {e}")
		return []


def default_tests(base="http://localhost:5009"):
	return [
		{
			"name": "Home page loads",
			"method": "GET",
			"url": f"{base}/",
			"status": 200,
			"text_contains": "Available Sources",
		},
		{
			"name": "Sources API",
			"method": "GET",
			"url": f"{base}/api/sources",
			"status": 200,
			"json_contains": {"0": None},  # presence: expect list-like JSON
		},
		{
			"name": "Content API",
			"method": "GET",
			"url": f"{base}/api/content",
			"status": 200,
		},
		{
			"name": "Missing content returns 404",
			"method": "GET",
			"url": f"{base}/api/content/99999999",
			"status": 404,
		},
	]


def main(argv):
	# Usage:
	# python auto_test.py [base_url] [tests.json]
	base = "http://localhost:5009"
	tests = None
	if len(argv) >= 2 and argv[1]:
		base = argv[1].rstrip("/")
	if len(argv) >= 3 and argv[2]:
		tests = load_tests_from_file(argv[2])
	if not tests:
		tests = default_tests(base)

	passed = 0
	failed = 0
	results = []
	for t in tests:
		if "url" in t and t["url"].startswith("/"):
			t["url"] = base + t["url"]
		ok, info = run_test(t)
		results.append((ok, info))
		if ok:
			passed += 1
			print(f"PASS - {info['name']} [{info['method']} {info['status']}] {info['url']}")
		else:
			failed += 1
			print(f"FAIL - {info['name']} [{info['method']} {info['status']}] {info['url']}")
			for f in info["failures"]:
				print("  -", f)

	print("\nSummary:")
	print(f"  Passed: {passed}")
	print(f"  Failed: {failed}")
	return 0 if failed == 0 else 1


if __name__ == "__main__":
	sys.exit(main(sys.argv))

