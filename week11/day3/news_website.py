from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder="news_templates", static_folder="news_templates")

# TheNewsAPI endpoint for top headlines
NEWS_API_URL = "https://api.thenewsapi.com/v1/news/top"


def load_api_key() -> str | None:
    """Load TheNewsAPI token from week11/news_api_key.txt (relative to this file)."""
    # Prefer key in week11/news_api_key.txt
    key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "news_api_key.txt"))
    if os.path.exists(key_path): # try to read it
        with open(key_path) as f:
            key = f.read().strip()
            return key or None # return key or None
    # Fallback: try a file next to this script
    local_path = os.path.join(os.path.dirname(__file__), "news_api_key.txt")
    if os.path.exists(local_path): 
        with open(local_path) as f:
            key = f.read().strip()
            return key or None
    return None


def fetch_top_headlines(locale: str = "us", limit: int = 10, category: str | None = None): 
    api_key = load_api_key()
    if not api_key:
        return None, "Missing TheNewsAPI key in week11/news_api_key.txt"

    params = { # request parameters
        "api_token": api_key,
        "locale": locale,
        "limit": max(1, min(int(limit or 10), 50)),  # clamp 1..50
    }
    if category: # add category if given
        params["categories"] = category

    try:  # make the API request
        response = requests.get(NEWS_API_URL, params=params, timeout=10)
    except requests.RequestException as e:
        return None, f"Network error: {e}"

    if response.status_code != 200:
        try:  # try to extract error message from JSON
            msg = response.json().get("message", response.text)
        except Exception:  # fallback if JSON parsing fails
            msg = response.text
        return None, f"API error ({response.status_code}): {msg}"

    try:  # parse JSON response
        data = response.json()
    except ValueError:
        return None, "Invalid JSON response from API."

    articles = data.get("data", []) # extract articles list
    if not isinstance(articles, list): # check if articles is a list
        return None, "Unexpected response shape: 'data' is not a list."

    return articles, None


@app.route("/", methods=["GET"])
def index():
    locale = (request.args.get("locale") or "us").lower()
    try:
        limit = int(request.args.get("limit") or 10)
    except ValueError:
        limit = 10

    # categories from query: comma-separated list
    raw_cats = (request.args.get("categories") or "").strip()
    categories = [c.strip().lower() for c in raw_cats.split(",") if c.strip()] or []

    if categories: # fetch per-category
        sections = {}  # dictionary to hold articles by category
        first_error = None
        for cat in categories:  # iterate over each category
            arts, err = fetch_top_headlines(locale=locale, limit=limit, category=cat)
            if err and not first_error:
                first_error = err
            sections[cat] = arts or []
        return render_template("index.html", sections=sections, error=first_error, locale=locale, limit=limit, categories=",".join(categories))
    else: # fetch general headlines
        articles, error = fetch_top_headlines(locale=locale, limit=limit)
        return render_template("index.html", articles=articles, error=error, locale=locale, limit=limit, categories="")


if __name__ == "__main__":
    app.run(debug=True)