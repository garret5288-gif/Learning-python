from flask import Flask, render_template, request
import os
import requests
from datetime import datetime, timedelta

app = Flask(__name__, template_folder="weather_templates", static_folder="weather_templates")

# Read the OpenWeather API key from week11/weather_api_key.txt
def load_api_key():
        try: # Load API key from file
                key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "weather_api_key.txt"))
                with open(key_path) as f:
                        key = f.read().strip()
        except FileNotFoundError: # File not found
                return None
        return key or None

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_forecast(city: str, api_key: str, limit: int = 5):
        try: # Make API request
                resp = requests.get(
                        FORECAST_URL,
                        params={"q": city, "appid": api_key, "units": "imperial"},
                        timeout=10,
                )
        except requests.RequestException as e: # handle network errors
                return None, f"Network error: {e}"

        if resp.status_code != 200: # handle API errors
                try:
                        msg = resp.json().get("message", resp.text)
                except Exception:
                        msg = resp.text
                return None, f"API error ({resp.status_code}): {msg}"

        data = resp.json() # parse JSON response
        items = data.get("list") or [] # forecast entries
        city_info = data.get("city") or {} # city information
        tz_offset = int(city_info.get("timezone") or 0)  # seconds offset from UTC
        rows = []
        for entry in items[:limit]: # iterate over forecast entries up to limit
                # Prefer UNIX timestamp + timezone for accurate local time
                when_txt = entry.get("dt_txt") or ""
                ts = entry.get("dt")
                if isinstance(ts, (int, float)):
                        dt_local = datetime.utcfromtimestamp(int(ts)) + timedelta(seconds=tz_offset)
                else:
                        # Fallback to parsing dt_txt (assumed UTC) then apply offset
                        try:
                                dt_utc = datetime.strptime(when_txt, "%Y-%m-%d %H:%M:%S")
                                dt_local = dt_utc + timedelta(seconds=tz_offset)
                        except Exception:
                                dt_local = None

                if dt_local is not None:
                        # Format as 12-hour time with AM/PM
                        when = dt_local.strftime("%I:%M %p").lstrip("0")
                else: # fallback to original text if parsing fails
                        when = when_txt
                main = entry.get("main") or {}
                weather_list = entry.get("weather") or [{}]
                desc = (weather_list[0] or {}).get("description", "")
                rows.append({
                        "when": when,
                        "temp": main.get("temp"),
                        "feels": main.get("feels_like"),
                        "desc": desc,
                })
        result = { # compile final result
                "city_name": (city_info.get("name") or city),
                "rows": rows,
                "count": len(rows),
                "total": len(items),
        }
        return result, None


@app.route("/", methods=["GET"])
def index(): # Main page route
        city = (request.args.get("city") or "").strip()
        error = None
        results = None

        if city: # if city provided, get forecast
                api_key = load_api_key()
                if not api_key: # Missing API key
                        error = "Missing OpenWeather API key in week11/weather_api_key.txt"
                else: # if API key loaded, get forecast
                        results, error = get_forecast(city, api_key, limit=5)

        return render_template("index.html", city=city, error=error, results=results)


if __name__ == "__main__":
        app.run(debug=True)
