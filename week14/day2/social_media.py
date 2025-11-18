from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib.parse import quote_plus
import io

app = Flask(__name__, template_folder="social_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
db = SQLAlchemy(app)

# Optional network client
try:
	import requests  # type: ignore
except Exception:  # pragma: no cover
	requests = None


def http_get_text(url: str, timeout: float = 6.0):
	if not requests:
		return None
	try:
		headers = {"User-Agent": "SocialAggregator/1.0 (+https://example.local)"}
		r = requests.get(url, headers=headers, timeout=timeout)
		r.raise_for_status()
		return r.text
	except Exception:
		return None


def parse_rss(text: str, source: str, limit: int = 10, default_author: str | None = None):
	items = []
	if not text:
		return items
	try:
		import xml.etree.ElementTree as ET
		# Handle common namespaces (media for thumbnails)
		ns = {
			'media': 'http://search.yahoo.com/mrss/',
			'atom': 'http://www.w3.org/2005/Atom'
		}
		root = ET.fromstring(text)
		# Try both RSS <item> and Atom <entry>
		candidates = root.findall('.//item')
		if not candidates:
			candidates = root.findall('.//{http://www.w3.org/2005/Atom}entry')

		def first_text(el, names):
			for name in names:
				child = el.find(name)
				if child is not None and (child.text or '').strip():
					return child.text.strip()
			return None

		def get_thumb(el):
			# media:thumbnail or media:content url
			thumb = el.find('media:thumbnail', ns)
			if thumb is not None and thumb.get('url'):
				return thumb.get('url')
			media_c = el.find('media:content', ns)
			if media_c is not None and media_c.get('url'):
				return media_c.get('url')
			return None

		def parse_dt(el):
			s = first_text(el, ['pubDate', 'published', 'updated', '{http://www.w3.org/2005/Atom}updated'])
			if not s:
				return None
			# Try a few common formats
			fmts = [
				'%a, %d %b %Y %H:%M:%S %z',  # RFC822
				'%Y-%m-%dT%H:%M:%S%z',       # ISO8601 with tz
				'%Y-%m-%dT%H:%M:%SZ',        # ISO Zulu
				'%Y-%m-%d %H:%M:%S',
			]
			for f in fmts:
				try:
					return datetime.strptime(s, f)
				except Exception:
					continue
			return None

		for el in candidates[:limit]:
			title = first_text(el, ['title', '{http://www.w3.org/2005/Atom}title']) or 'Untitled'
			link = first_text(el, ['link'])
			if link is None:
				# Atom link is attribute href
				l = el.find('{http://www.w3.org/2005/Atom}link')
				if l is not None and l.get('href'):
					link = l.get('href')
			author = first_text(el, ['author', '{http://www.w3.org/2005/Atom}author']) or default_author or source
			if isinstance(author, str) and not author.strip():
				author = default_author or source
			thumb = get_thumb(el)
			dt = parse_dt(el)
			items.append({
				'source': source,
				'title': title,
				'author': author if isinstance(author, str) else default_author or source,
				'url': link or '#',
				'created_at': dt,
				'thumbnail': thumb,
			})
	except Exception:
		return []
	return items


def fetch_reddit(subreddit: str, limit: int = 8):
	sub = (subreddit or '').strip().lstrip('r/') or 'python'
	url = f"https://www.reddit.com/r/{quote_plus(sub)}/.rss"
	text = http_get_text(url)
	posts = parse_rss(text or '', source='reddit', limit=limit, default_author=f"r/{sub}")
	if not posts:
		posts = [{
			'source': 'reddit', 'title': f'r/{sub} example post', 'author': f'r/{sub}',
			'url': f'https://www.reddit.com/r/{sub}/', 'created_at': datetime.now(), 'thumbnail': None
		}]
	return posts


def fetch_youtube(channel_id: str, limit: int = 6):
	cid = (channel_id or '').strip()
	if not cid:
		# Google Developers as default sample
		cid = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
	url = f"https://www.youtube.com/feeds/videos.xml?channel_id={quote_plus(cid)}"
	text = http_get_text(url)
	posts = parse_rss(text or '', source='youtube', limit=limit, default_author='YouTube')
	if not posts:
		posts = [{
			'source': 'youtube', 'title': 'Sample video', 'author': 'YouTube',
			'url': 'https://www.youtube.com/', 'created_at': datetime.now(), 'thumbnail': None
		}]
	return posts


def fetch_generic_rss(url: str, limit: int = 6):
	clean = (url or '').strip()
	if not clean:
		return []
	text = http_get_text(clean)
	posts = parse_rss(text or '', source='rss', limit=limit, default_author='RSS')
	return posts


@app.route('/')
def home():
	# Configure sources via query params
	subs_raw = request.args.get('subs', 'python, flask')
	channels_raw = request.args.get('channels', 'UC_x5XG1OV2P6uZZ5FSM9Ttw')
	rss_raw = request.args.get('rss', '')
	limit = request.args.get('limit', type=int) or 10

	subs = [s.strip() for s in subs_raw.split(',') if s.strip()][:5]
	chans = [c.strip() for c in channels_raw.split(',') if c.strip()][:5]
	rss_urls = [u.strip() for u in rss_raw.replace('\n', ',').split(',') if u.strip()][:5]

	posts = []
	for s in subs:
		posts.extend(fetch_reddit(s, limit=limit))
	for c in chans:
		posts.extend(fetch_youtube(c, limit=min(6, limit)))
	for u in rss_urls:
		posts.extend(fetch_generic_rss(u, limit=min(6, limit)))

	# Sort newest first; None dates go last
	def sort_key(p):
		return p.get('created_at') or datetime.min
	posts.sort(key=sort_key, reverse=True)

	return render_template('feed.html', posts=posts, subs=subs, channels=chans, rss_urls=rss_urls, limit=limit)


if __name__ == '__main__':
	app.run(debug=True, port=5003)