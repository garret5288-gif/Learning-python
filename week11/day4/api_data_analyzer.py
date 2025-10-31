
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


@dataclass
class Geo:
	name: str
	country: Optional[str]
	latitude: float
	longitude: float
	timezone: Optional[str]


def geocode_city(city: str, country_code: Optional[str] = None, limit: int = 1) -> Optional[Geo]:
	params = {"name": city, "count": limit}
	if country_code:
		params["country"] = country_code
	try:
		r = requests.get(GEOCODE_URL, params=params, timeout=15)
		r.raise_for_status()
		data = r.json()
	except requests.RequestException as e:
		print(f"Geocoding error: {e}")
		return None

	results = (data or {}).get("results") or []
	if not results:
		print("No geocoding results.")
		return None
	top = results[0]
	return Geo(
		name=top.get("name") or city,
		country=top.get("country"),
		latitude=float(top.get("latitude")),
		longitude=float(top.get("longitude")),
		timezone=top.get("timezone"),
	)


def _request_daily(url: str, lat: float, lon: float, start: date, end: date, timezone: Optional[str], daily: List[str]) -> Dict:
	# Only the variables we need for a simple analysis
	params = {
		"latitude": lat,
		"longitude": lon,
		"daily": ",".join(daily),
		"start_date": start.isoformat(),
		"end_date": end.isoformat(),
		"timezone": timezone or "auto",
	}
	try:
		r = requests.get(url, params=params, timeout=20)
		r.raise_for_status()
		return r.json() or {}
	except requests.RequestException as e:
		print(f"Fetch error: {e}")
		return {}


def _merge_daily(a: Dict, b: Dict) -> Dict:
	if not a:
		return b or {}
	if not b:
		return a or {}
	out = {}
	# time is the index; simply concatenate preserving order
	ta = a.get("time") or []
	tb = b.get("time") or []
	out["time"] = list(ta) + list(tb)
	keys = set(a.keys()) | set(b.keys())
	keys.discard("time")
	for k in keys:
		va = a.get(k) or []
		vb = b.get(k) or []
		out[k] = list(va) + list(vb)
	return out


def fetch_daily_weather(lat: float, lon: float, start: date, end: date, timezone: Optional[str]) -> Dict:
	# Only the variables we need for a simple analysis
	daily_keys = [
		"temperature_2m_max",
		"temperature_2m_min",
		"precipitation_sum",
		"windspeed_10m_max",
	]

	today = datetime.utcnow().date()
	if end < today:
		# Entirely in the past -> Archive API
		payload = _request_daily(ARCHIVE_URL, lat, lon, start, end, timezone, daily_keys)
		return (payload or {}).get("daily") or {}
	elif start >= today:
		# Today/future -> Forecast API
		payload = _request_daily(FORECAST_URL, lat, lon, start, end, timezone, daily_keys)
		return (payload or {}).get("daily") or {}
	else:
		# Spans past and today/future: split and merge (archive up to yesterday, forecast from today)
		past_end = today - timedelta(days=1)
		arch = _request_daily(ARCHIVE_URL, lat, lon, start, past_end, timezone, daily_keys) if start <= past_end else {}
		frc = _request_daily(FORECAST_URL, lat, lon, today, end, timezone, daily_keys)
		daily_arch = (arch or {}).get("daily") or {}
		daily_frc = (frc or {}).get("daily") or {}
		return _merge_daily(daily_arch, daily_frc)


def to_records(daily: Dict) -> List[Dict]:
	if not daily:
		return []
	times = daily.get("time") or []
	tmax = daily.get("temperature_2m_max") or []
	tmin = daily.get("temperature_2m_min") or []
	precip = daily.get("precipitation_sum") or []
	windmax = daily.get("windspeed_10m_max") or []

	recs: List[Dict] = []
	for i, ts in enumerate(times):
		vmax = tmax[i] if i < len(tmax) else None
		vmin = tmin[i] if i < len(tmin) else None
		temp_avg = None
		if isinstance(vmax, (int, float)) and isinstance(vmin, (int, float)):
			temp_avg = round((float(vmax) + float(vmin)) / 2.0, 2)
		row = {
			"date": ts,
			"temp_avg": temp_avg,
			"precipitation": precip[i] if i < len(precip) else None,
			"wind_max": windmax[i] if i < len(windmax) else None,
		}
		recs.append(row)
	return recs


def summarize(recs: List[Dict]) -> Dict:
	temps = [float(r["temp_avg"]) for r in recs if isinstance(r.get("temp_avg"), (int, float))]
	precs = [float(r["precipitation"]) for r in recs if isinstance(r.get("precipitation"), (int, float))]
	winds = [float(r["wind_max"]) for r in recs if isinstance(r.get("wind_max"), (int, float))]

	def avg(xs: List[float]) -> Optional[float]:
		return round(sum(xs) / len(xs), 2) if xs else None

	return {
		"avg_temp": avg(temps),
		"total_precip": round(sum(precs), 2) if precs else None,
		"avg_wind": avg(winds),
	}


def prompt(text: str, default: Optional[str] = None) -> str:
	suffix = f" [{default}]" if default else ""
	val = input(f"{text}{suffix}: ").strip()
	return val or (default or "")


def main():
	print("Open‑Meteo Analyzer")
	city = prompt("City", "Dallas")
	cc = prompt("Country code (optional)", "US")
	start_s = prompt("Start date (YYYY-MM-DD)", "2024-01-01")
	end_s = prompt("End date (YYYY-MM-DD)", datetime.utcnow().date().isoformat())

	try:
		start_d = datetime.strptime(start_s, "%Y-%m-%d").date()
		end_d = datetime.strptime(end_s, "%Y-%m-%d").date()
		if end_d < start_d:
			start_d, end_d = end_d, start_d
	except ValueError:
		print("Invalid dates.")
		return

	geo = geocode_city(city, cc or None)
	if not geo:
		return

	daily = fetch_daily_weather(geo.latitude, geo.longitude, start_d, end_d, geo.timezone)
	recs = to_records(daily)
	if not recs:
		print("No daily records returned.")
		return

	summary = summarize(recs)
	out = {
		"meta": {
			"source": "open-meteo",
			"generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
		},
		"query": {
			"city": geo.name,
			"country": geo.country,
			"latitude": geo.latitude,
			"longitude": geo.longitude,
			"timezone": geo.timezone,
			"start": start_d.isoformat(),
			"end": end_d.isoformat(),
		},
		"summary": summary,
		"records": recs,
	}

	out_name = prompt("Save to JSON filename", "open_meteo_analysis.json")
	try:
		Path(out_name).write_text(json.dumps(out, indent=2), encoding="utf-8")
		print(f"Saved {len(recs)} records to {out_name}")
	except OSError as e:
		print(f"Failed to write file: {e}")


if __name__ == "__main__":
	main()