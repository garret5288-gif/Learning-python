from flask import Flask, render_template
import requests
import json

app = Flask(__name__, template_folder="templates", static_folder="templates")

QUOTE_API_URL = "https://api.quotable.io/random"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
NEWS_API_URL = "https://api.thenewsapi.com/v1/news/top"


weather_key_path = "weather_api_key.txt"
news_key_path = "news_api_key.txt"

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

def fetch_random_quote():
    try:
        response = requests.get(QUOTE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        quote = data.get("content")
        author = data.get("author")
        if quote and author:
            return f'"{quote}" — {author}'
        return "No quote found."
    except requests.RequestException as e:
        return f"Error fetching quote: {e}"
    
def get_current_weather(city: str, api_key: str):
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
            return f"{temp}°F, {description.capitalize()}"
        return "Weather data not found."
    except requests.RequestException as e:
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
        headlines = [a.get("title") or "(No Title)" for a in articles]
        return headlines
    except requests.RequestException as e:
        return [f"Error fetching news: {e}"]
    
def get_forecast(city: str, api_key: str, limit: int = 5):
    try:
        response = requests.get(
            FORECAST_URL,
            params={"q": city, "appid": api_key, "units": "imperial"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        items = data.get("list") or []
        forecasts = []
        for entry in items[:limit]:
            when_txt = entry.get("dt_txt") or ""
            temp = entry.get("main", {}).get("temp")
            desc = entry.get("weather", [{}])[0].get("description", "")
            forecasts.append(f"{when_txt}: {temp}°F, {desc.capitalize()}")
        return forecasts
    except requests.RequestException as e:
        return [f"Error fetching forecast: {e}"]
    
@app.route('/')
def index():
    quote = fetch_random_quote()
    weather_api_key = load_weather_api_key()
    news_api_key = load_news_api_key()
    
    weather = get_current_weather("New York", weather_api_key) if weather_api_key else "No API key for weather."
    headlines = get_top_headlines(news_api_key) if news_api_key else ["No API key for news."]
    forecast = get_forecast("New York", weather_api_key) if weather_api_key else ["No API key for forecast."]
    
    return render_template("index.html", quote=quote, weather=weather, headlines=headlines, forecast=forecast)    



if __name__ == "__main__":
    app.run(debug=True)
