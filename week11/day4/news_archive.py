import requests
import json

NEWS_API_URL = "https://api.thenewsapi.com/v1/news/top"

API_KEY_PATH = "news_api_key.txt"

def load_api_key():
    try: # Load News API key from file
        with open(API_KEY_PATH) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    
def get_top_headlines(api_key, limit=5, locale="us"):
    try: # Fetch top headlines from TheNewsAPI
        resp = requests.get(
            NEWS_API_URL,
            params={"api_token": api_key, "limit": limit, "locale": locale},
            timeout=10,
        )
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None

    if resp.status_code != 200:
        try: # handle API errors
            err = resp.json()
            msg = err.get("message") or err
        except Exception:
            msg = resp.text
        print(f"API error ({resp.status_code}): {msg}")
        return None

    data = resp.json() # parse JSON response
    return data.get("data") or []


def read_archive(path):
    try: # Read archived news articles from file
        with open(path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def write_archive(path, items):
    with open(path, "w") as f: # Write archived news articles to file
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")


def print_headlines(articles): # Print a numbered list of headlines
    for i, a in enumerate(articles, 1):
        title = a.get("title") or "(No Title)"
        source = a.get("source") or a.get("source_url") or "Unknown"
        url = a.get("url") or ""
        line = f"{i}. {title} ({source})"
        if url:
            line += f"\n   {url}"
        print(line)


def parse_selection(text, count): # Parse user selection input into list of indices
    text = (text or "").strip().lower()
    if not text:
        return []
    if text in ("a", "all"):
        return list(range(1, count + 1))
    sel = set()
    parts = [p.strip() for p in text.split(",") if p.strip()]
    for p in parts:
        if "-" in p:
            try: # handle ranges
                start, end = p.split("-", 1)
                s, e = int(start), int(end)
                if s <= e:
                    for n in range(s, e + 1):
                        if 1 <= n <= count:
                            sel.add(n)
            except ValueError:
                continue
        else: # handle single numbers
            try:
                n = int(p)
                if 1 <= n <= count:
                    sel.add(n)
            except ValueError:
                continue
    return sorted(sel)

def menu():
    print("News Archive Menu:")
    print("1. Fetch Top Headlines")
    print("2. View Saved Headlines")
    print("3. Clear Saved Headlines")
    print("4. Exit")

def main():
    api_key = load_api_key()
    if not api_key:
        print(f"Missing API key file: {API_KEY_PATH}. Create it and put your News API key inside.")
        return
    archive_file = "news_archive.json"
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            headlines = get_top_headlines(api_key)
            if headlines is None: # error occurred
                continue
            if not headlines: # no headlines found
                print("(no headlines)")
                continue
            print("\nTop Headlines:\n")
            print_headlines(headlines)
            count = len(headlines)
            sel_text = input(f"\nEnter numbers to save (1-{count}) or 'a' for all, or Enter to skip: ")
            idxs = parse_selection(sel_text, len(headlines))
            if not idxs:
                print("No headlines saved.")
                continue
            to_save = [headlines[i - 1] for i in idxs]
            existing = read_archive(archive_file)
            # dedupe by URL if present, else by title
            seen_urls = {item.get("url") for item in existing if isinstance(item, dict)}
            seen_titles = {item.get("title") for item in existing if isinstance(item, dict)}
            appended = 0
            for art in to_save: # append if not duplicate
                url = art.get("url")
                title = art.get("title")
                if url and url in seen_urls:
                    continue
                if (not url) and title and title in seen_titles:
                    continue
                existing.append(art)
                if url:
                    seen_urls.add(url)
                if title:
                    seen_titles.add(title)
                appended += 1
            write_archive(archive_file, existing)
            print(f"Saved {appended} headline(s) to {archive_file}.")
        elif choice == "2":
            try:
                with open(archive_file, "r") as f:
                    saved_headlines = json.load(f)
                    if not saved_headlines:
                        print("No saved headlines.")
                        continue
                    for i, article in enumerate(saved_headlines, 1): # display saved headlines
                        title = article.get("title") or "No Title"
                        source = article.get("source") or article.get("source_url") or "Unknown"
                        url = article.get("url") or ""
                        line = f"{i}. {title} ({source})"
                        if url:
                            line += f"\n   {url}"
                        print(line)
            except FileNotFoundError:
                print("No saved headlines found.")
        elif choice == "3":
            write_archive(archive_file, [])
            print("Cleared saved headlines.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()