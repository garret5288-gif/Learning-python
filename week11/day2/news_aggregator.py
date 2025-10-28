import requests

try:
    api_key = open("news_api_key.txt").read().strip()
except FileNotFoundError:
    raise SystemExit("Missing API key file: news_api_key.txt. Create it and put your TheNewsAPI token inside.")

if not api_key:
    raise SystemExit("Empty API token in news_api_key.txt")

# TheNewsAPI top headlines endpoint
base_url = "https://api.thenewsapi.com/v1/news/top"

print("Latest News Headlines:")

# Network call with error handling
try:
    response = requests.get(
        base_url,
        params={"api_token": api_key, "locale": "us", "limit": 5},
        timeout=10,
    )
except requests.RequestException as e:
    raise SystemExit(f"Network error: {e}")

# Status code handling
if response.status_code != 200:
    try:
        err = response.json()
        msg = err.get("message") or err
    except Exception:
        msg = response.text
    raise SystemExit(f"API error ({response.status_code}): {msg}")

# Safe JSON parsing
try:
    data = response.json()
except ValueError:
    raise SystemExit("Invalid JSON response from API.")

articles = data.get("data", [])
if not isinstance(articles, list):
    raise SystemExit("Unexpected response shape: 'data' is not a list.")

if not articles:
    print("(no articles)")
else:
    for article in articles:
        title = article.get("title", "No Title")
        source = article.get("source", "Unknown Source")
        url = article.get("url")
        line = f"- {title} ({source})"
        if url:
            line += f"\n  {url}"
        print(line)