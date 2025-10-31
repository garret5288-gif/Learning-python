from flask import Flask, render_template
import requests
import json

app = Flask(__name__, template_folder="templates", static_folder="templates")

QUOTE_API_URL = "https://api.quotable.io/random"
ZEN_API_URL = "https://zenquotes.io/api/random"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
NEWS_API_URL = "https://api.thenewsapi.com/v1/news/top"


weather_key_path = "weather_api_key.txt"
news_key_path = "news_api_key.txt"

# --- Simple JSON file cache with TTL (no extra imports) ---
CACHE_FILE = "weather_cache.json"  # created in current working directory
# TTLs in seconds
CURRENT_WEATHER_TTL = 5 * 60   # 5 minutes
DAILY_FORECAST_TTL = 30 * 60   # 30 minutes
try:
    import time  # allowed stdlib import
except Exception:
    time = None

def _load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"current_weather": {}, "forecast": {}}
            data.setdefault("current_weather", {})
            data.setdefault("forecast", {})
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"current_weather": {}, "forecast": {}}

def _save_cache(cache):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except OSError:
        # If we can't write, just skip caching silently
        pass

def _make_key(city, units="imperial"):
    city = (city or "").strip().lower()
    return f"{city}|{units}"

def load_weather_api_key():
    try:
        with open(weather_key_path) as f:
            key = f.read().strip()
    except FileNotFoundError:  # File not found
        return None
    return key or None

def load_news_api_key():
    try:
        with open(news_key_path) as f:
            key = f.read().strip()
    except FileNotFoundError:  # File not found
        return None
    return key or None

def fetch_random_quote(tag: str | None = None) -> tuple[str | None, str | None]:
    """Fetch a random quote from Quotable, fallback to ZenQuotes on failure."""
    # Try Quotable first (supports tags)
    try:
        params = {"tags": tag} if tag else None
        response = requests.get(QUOTE_API_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            quote = data.get("content")
            author = data.get("author")
            if quote and author: # valid quote
                return f'"{quote}" — {author}', None
        # If non-200 or malformed, fall through to ZenQuotes
    except requests.RequestException:
        pass # network error, fall through
    except ValueError:
        pass # malformed JSON, fall through

    # Fallback: ZenQuotes (no tag filter)
    try:
        resp2 = requests.get(ZEN_API_URL, timeout=10)
    except requests.RequestException as e:
        return None, f"Network error: {e}"

    if resp2.status_code != 200:
        return None, f"API error ({resp2.status_code}): {resp2.text}"

    try:  # parse JSON response from fallback
        data2 = resp2.json()
        if isinstance(data2, list) and data2:
            item = data2[0] or {}
            q = item.get("q")
            a = item.get("a")
            if q and a:
                return f'"{q}" — {a}', None
        return None, "Malformed response from fallback API."
    except ValueError:
        return None, "Invalid JSON response from fallback API."


def get_current_weather(city: str, api_key: str):
    # Try cache first with TTL
    cache = _load_cache()
    key = _make_key(city, "imperial")
    cached_entry = cache["current_weather"].get(key)
    if cached_entry:
        # Backward compat: old cache stored a plain string
        if isinstance(cached_entry, str):
            return cached_entry
        # New format: {"value": str, "ts": float}
        ts = cached_entry.get("ts")
        if time and isinstance(ts, (int, float)) and (time.time() - ts) < CURRENT_WEATHER_TTL:
            return cached_entry.get("value")

    # Fetch and cache
    try:
        response = requests.get(
            CURRENT_WEATHER_URL,
            params={"q": city, "appid": api_key, "units": "imperial"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        temp = data.get("main", {}).get("temp")
        description = data.get("weather", [{}])[0].get("description")
        if temp is not None and description:
            value = f"{temp}°F, {description.capitalize()}"
            cache["current_weather"][key] = {"value": value, "ts": time.time() if time else 0}
            _save_cache(cache)
            return value
        return "Weather data not found."
    except requests.RequestException as e:
        # If API fails but we somehow have cache, return it; else return error
        if cached_entry:
            return cached_entry if isinstance(cached_entry, str) else cached_entry.get("value")
        return f"Error fetching weather: {e}"
    
def get_top_headlines(api_key, limit=5, locale="us"):
    try:
        response = requests.get(
            NEWS_API_URL,
            params={"api_token": api_key, "limit": limit, "locale": locale},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        articles = data.get("data") or []
        # Return list of dicts with title and url
        items = []
        for a in articles:
            title = a.get("title") or "(No Title)"
            url = a.get("url") or "#"
            items.append({"title": title, "url": url})
        return items
    except requests.RequestException as e:
        return [{"title": f"Error fetching news: {e}", "url": "#"}]
    
def get_forecast(city: str, api_key: str, days: int = 5):
    # Try cache first (no TTL) using a distinct key for daily aggregation
    cache = _load_cache()
    key = _make_key(city, "imperial") + f"|days={days}|daily"
    cached_entry = cache["forecast"].get(key)
    if cached_entry:
        # Backward compat: old cache stored a list of strings
        if isinstance(cached_entry, list):
            return cached_entry
        ts = cached_entry.get("ts")
        if time and isinstance(ts, (int, float)) and (time.time() - ts) < DAILY_FORECAST_TTL:
            return cached_entry.get("value") or []

    # Fetch 3-hourly data and aggregate into daily summaries
    try:
        response = requests.get(
            FORECAST_URL,
            params={"q": city, "appid": api_key, "units": "imperial"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("list") or []

        # Group by date (YYYY-MM-DD)
        daily = {}
        for entry in items:
            when_txt = entry.get("dt_txt") or ""
            if len(when_txt) < 10:
                continue
            day = when_txt[:10]
            temp = entry.get("main", {}).get("temp")
            desc = entry.get("weather", [{}])[0].get("description", "")
            if temp is None:
                continue
            bucket = daily.setdefault(day, {"temps": [], "descs": []})
            bucket["temps"].append(temp)
            if desc:
                bucket["descs"].append(desc)

        summaries = []
        for day in sorted(daily.keys())[:days]:
            temps = daily[day]["temps"]
            descs = daily[day]["descs"]
            hi = max(temps)
            lo = min(temps)
            # Pick the most frequent description; fallback to first or Unknown
            rep = "Unknown"
            if descs:
                counts = {}
                for d in descs:
                    counts[d] = counts.get(d, 0) + 1
                rep = max(counts.items(), key=lambda x: x[1])[0].capitalize()
            summaries.append(f"{day}: High {hi}°F, Low {lo}°F, {rep}")

        cache["forecast"][key] = {"value": summaries, "ts": time.time() if time else 0}
        _save_cache(cache)
        return summaries
    except requests.RequestException as e:
        if cached_entry:
            return cached_entry if isinstance(cached_entry, list) else (cached_entry.get("value") or [])
        return [f"Error fetching forecast: {e}"]
    
@app.route('/')
def index():
    quote = fetch_random_quote()
    weather_api_key = load_weather_api_key()
    news_api_key = load_news_api_key()

    city = "tampa"
    weather = get_current_weather(city, weather_api_key) if weather_api_key else "No API key for weather."
    headlines = get_top_headlines(news_api_key) if news_api_key else [{"title": "No API key for news.", "url": "#"}]
    forecast = get_forecast(city, weather_api_key) if weather_api_key else ["No API key for forecast."]

    return render_template("index.html", quote=quote, city=city.title(), weather=weather, headlines=headlines, forecast=forecast)



if __name__ == "__main__":
    app.run(debug=True)
