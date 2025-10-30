import json
import requests

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
key_path = "weather_api_key.txt"

def load_api_key(): # Load OpenWeather API key from file
    try:
        with open(key_path) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None 

def menu(): # Display menu options
    print("Weather Logger Menu:")
    print("1. Find and log weather")
    print("2. View Logged Data")
    print("3. Exit")


def _read_log_entries(path): # Return a list of logged entries.
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            if content.lstrip().startswith("["):
                try: # Try parsing as a pretty JSON array
                    data = json.loads(content)
                    if isinstance(data, list):
                        return data
                except json.JSONDecodeError:
                    pass
            # Fallback: NDJSON (one JSON object per line)
            items = []
            for line in content.splitlines(): # process each line
                line = line.strip()
                if not line:
                    continue
                try: # parse each line as JSON
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    # skip malformed lines
                    continue
            return items
    except FileNotFoundError:
        return []


def _append_pretty(path, obj): # Append an object to a pretty-printed JSON array on disk.
    entries = _read_log_entries(path)
    entries.append(obj) # append new object
    with open(path, "w") as f: # write updated list
        json.dump(entries, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def _simplify_forecast(data): # Extract only the requested fields from OpenWeather forecast data.
    city = (data or {}).get("city") or {}
    items = (data or {}).get("list") or []
    first = items[0] if items else {}
    main = first.get("main") or {}
    clouds = first.get("clouds") or {}
    rain_obj = first.get("rain") or {}

    # Prefer 3h rainfall, then 1h
    rain_val = None
    if isinstance(rain_obj, dict):
        rain_val = rain_obj.get("3h")
        if rain_val is None:
            rain_val = rain_obj.get("1h")

    return { # Extracted fields
        "country": city.get("country"),
        "city": city.get("name"),
        "time": first.get("dt_txt") or first.get("dt"),
        "temp": main.get("temp"),
        "clouds": clouds.get("all"),
        "rain": rain_val,
    }

def main(): # Main program loop
    api_key = load_api_key()
    if not api_key: # No API key found
        print(f"Missing API key file: {key_path}. Create it and put your OpenWeather key inside.")
        return
    log_file = "weather_log.json"
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            city = input("Enter city name: ").strip()
            try: # Fetch weather data from OpenWeather API
                resp = requests.get(
                    FORECAST_URL,
                    params={"q": city, "appid": api_key, "units": "imperial"},
                    timeout=10,
                )
                resp.raise_for_status()
                raw = resp.json()
                simplified = _simplify_forecast(raw)
                _append_pretty(log_file, simplified)
                print(f"Logged weather data for {simplified.get('city') or city}.")
            except requests.RequestException as e:
                print(f"Error fetching weather data: {e}")
        elif choice == "2": # View logged data
            entries = _read_log_entries(log_file)
            if not entries:
                print("No logged data found.")
                continue
            for i, entry in enumerate(entries, 1):
                # New minimal format
                if isinstance(entry.get("city"), str):
                    city_name = entry.get("city") or "Unknown"
                    country = entry.get("country") or ""
                    time_val = entry.get("time") or ""
                    temp = entry.get("temp")
                    clouds = entry.get("clouds")
                    rain = entry.get("rain")
                    print(f"\nEntry {i}: {city_name}, {country}")
                    print(f"  time: {time_val}, temp: {temp}°F, clouds: {clouds}%, rain: {rain if rain is not None else 0}")
                else:
                    # Legacy full format
                    city_name = entry.get("city", {}).get("name", "Unknown")
                    country = entry.get("city", {}).get("country", "")
                    print(f"\nEntry {i}: {city_name}, {country}")
                    items = entry.get("list", [])
                    for item in items[:5]:  # Show first 5 forecast entries
                        dt_txt = item.get("dt_txt", "")
                        main = item.get("main", {})
                        temp = main.get("temp", "N/A")
                        clouds = (item.get("clouds") or {}).get("all")
                        rain_obj = item.get("rain") or {}
                        rain = rain_obj.get("3h", rain_obj.get("1h", 0))
                        print(f"  {dt_txt}: {temp}°F, clouds {clouds}%, rain {rain}")
        elif choice == "3":
            print("Exiting Weather Logger.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()