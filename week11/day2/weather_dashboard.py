import requests

# Load API key from current working directory (run from week11/)
key_path = "weather_api_key.txt"
try:
    api_key = open(key_path).read().strip()
except FileNotFoundError:
    raise SystemExit(f"Missing API key file: {key_path}. Create it and put your OpenWeather key inside.")

# Use 5-day / 3-hour forecast endpoint (free tier) with imperial units for °F
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


def forecast(city: str) -> None:
    """Print a simple multi-slot forecast for the given city (°F)."""
    try:
        resp = requests.get(
            BASE_URL,
            params={"q": city, "appid": api_key, "units": "imperial"},
            timeout=10,
        )
    except requests.RequestException as e:
        print(f"{city}: network error: {e}")
        return

    if resp.status_code != 200:
        # Show API error message if present
        try:
            err = resp.json()
            msg = err.get("message") or err
        except Exception:
            msg = resp.text
        print(f"{city}: API error ({resp.status_code}): {msg}")
        return

    data = resp.json()
    city_info = data.get("city") or {}
    name = city_info.get("name") or city
    country = city_info.get("country") or ""
    where = f"{name}{(', ' + country) if country else ''}"
    print(where)

    items = data.get("list") or []
    if not items:
        print("  No forecast data available.")
        return

    # Show the next 5 forecast slots (each is a 3-hour step)
    for entry in items[:5]:
        dt_txt = entry.get("dt_txt") or ""
        main = entry.get("main") or {}
        weather_list = entry.get("weather") or [{}]
        desc = (weather_list[0] or {}).get("description", "")
        temp = main.get("temp")
        feels = main.get("feels_like")
        line = f"  {dt_txt}: {temp}°F"
        if feels is not None:
            line += f" (feels {feels}°F)"
        if desc:
            line += f", {desc}"
        print(line)


if __name__ == "__main__":
    for city in ["plant city", "miami", "orlando"]:
        forecast(city)

