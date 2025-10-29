from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="random_quote_templates", static_folder="random_quote_templates")
# Quotable API endpoint and ZenQuotes fallback
QUOTE_API_URL = "https://api.quotable.io/random"
ZEN_API_URL = "https://zenquotes.io/api/random"


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


@app.route('/')
def index():
    tag = (request.args.get("tag") or "").strip() or None
    quote, error = fetch_random_quote(tag) # Fetch quote with optional tag
    return render_template("index.html", quote=quote, error=error, tag=request.args.get("tag") or "")

if __name__ == "__main__":
    app.run(debug=True)