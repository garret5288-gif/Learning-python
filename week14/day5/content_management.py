from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.request, urllib.error, xml.etree.ElementTree as ET, json
from email.utils import parsedate_to_datetime

app = Flask(__name__, template_folder="cms_templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cms.db'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
db = SQLAlchemy(app)

class Source(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	url = db.Column(db.String(500), nullable=False)
	kind = db.Column(db.String(50), nullable=False)  # rss | json
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContentItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
	title = db.Column(db.String(300), nullable=False)
	summary = db.Column(db.Text)
	link = db.Column(db.String(500))
	published_at = db.Column(db.DateTime, default=datetime.utcnow)
	raw = db.Column(db.Text)  # JSON blob of original
	source = db.relationship('Source', backref=db.backref('items', lazy='dynamic'))

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)

class ItemTag(db.Model):
	item_id = db.Column(db.Integer, db.ForeignKey('content_item.id'), primary_key=True)
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

def ensure_schema():
	with app.app_context():
		db.create_all()

def seed_default_sources():
	"""Insert a few starter sources if database is empty."""
	with app.app_context():
		if Source.query.count() > 0:
			return 0
		# Sample public feeds (replace or remove later if desired)
		seeds = [
			{"name": "Python.org News", "url": "https://www.python.org/blogs/rss", "kind": "rss"},
			{"name": "CNN Top Stories", "url": "http://rss.cnn.com/rss/cnn_topstories.rss", "kind": "rss"},
			{"name": "HN Front Page (Algolia JSON)", "url": "https://hn.algolia.com/api/v1/search?tags=front_page", "kind": "json"},
			{"name": "BBC World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "kind": "rss"},
			{"name": "Reuters Technology", "url": "https://feeds.reuters.com/reuters/technologyNews", "kind": "rss"},
			{"name": "NYTimes Technology", "url": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml", "kind": "rss"},
			{"name": "NASA Breaking News", "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss", "kind": "rss"},
			{"name": "Public APIs (JSON sample)", "url": "https://api.publicapis.org/entries", "kind": "json"},
		]
		added = 0
		for s in seeds:
			if not Source.query.filter_by(url=s['url']).first():
				db.session.add(Source(name=s['name'], url=s['url'], kind=s['kind']))
				added += 1
		db.session.commit()
		return added

USER_AGENT = "SimpleCMS/1.0 (+https://example.local)"

def _open(url: str):
	req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
	return urllib.request.urlopen(req, timeout=10)

def fetch_rss(url: str):
	"""Fetch and parse a simple RSS feed returning list of dicts."""
	try:
		with _open(url) as resp:
			data = resp.read().decode('utf-8', 'ignore')
	except Exception:
		return []
	try:
		root = ET.fromstring(data)
	except Exception:
		return []
	items = []
	for item in root.findall('.//item'):
		title = (item.findtext('title') or '').strip() or 'Untitled'
		link = (item.findtext('link') or '').strip()
		desc = (item.findtext('description') or '').strip()
		pub_raw = (item.findtext('pubDate') or '').strip()
		# Attempt RFC822 parsing
		pub_dt = None
		if pub_raw:
			try:
				pub_dt = parsedate_to_datetime(pub_raw)
			except Exception:
				pub_dt = None
		items.append({'title': title, 'summary': desc, 'link': link, 'published': pub_raw, 'published_dt': pub_dt})
	return items

def fetch_json(url: str):
	"""Fetch a JSON array of objects and map to content items."""
	try:
		with _open(url) as resp:
			raw = resp.read().decode('utf-8', 'ignore')
			data = json.loads(raw)
	except Exception:
		return []
	if not isinstance(data, list):
		return []
	out = []
	for obj in data:
		if not isinstance(obj, dict):
			continue
		out.append({
			'title': str(obj.get('title') or obj.get('name') or 'Untitled'),
			'summary': str(obj.get('summary') or obj.get('description') or '')[:500],
			'link': str(obj.get('url') or ''),
			'published': str(obj.get('published') or obj.get('date') or ''),
			'raw': obj
		})
	return out

def ingest_source(source: Source):
	"""Pull entries from a source and store new ones."""
	if source.kind == 'rss':
		entries = fetch_rss(source.url)
	elif source.kind == 'json':
		entries = fetch_json(source.url)
	else:
		entries = []
	new_count = 0
	for e in entries[:50]:  # limit
		title = (e.get('title') or 'Untitled').strip()
		if not title:
			continue
		if ContentItem.query.filter_by(source_id=source.id, title=title).first():
			continue
		pub_dt = e.get('published_dt') if 'published_dt' in e else None
		item = ContentItem(
			source_id=source.id,
			title=title[:300],
			summary=(e.get('summary') or '')[:2000],
			link=e.get('link') or None,
			published_at=pub_dt or datetime.utcnow(),
			raw=json.dumps(e)
		)
		db.session.add(item)
		new_count += 1
	db.session.commit()
	return new_count

@app.route('/')
def index():
	ensure_schema()
	seed_default_sources()
	latest = ContentItem.query.order_by(ContentItem.published_at.desc()).limit(25).all()
	# Auto-ingest if no items yet but sources exist
	if not latest and Source.query.count() > 0:
		for s in Source.query.all():
			try:
				ingest_source(s)
			except Exception:
				pass
		latest = ContentItem.query.order_by(ContentItem.published_at.desc()).limit(25).all()
	return render_template('items.html', items=latest, sources=Source.query.all(), title='Latest')

@app.route('/sources', methods=['GET','POST'])
def sources():
	ensure_schema()
	# Do not reseed automatically here, but sources show seeded ones
	if request.method == 'POST':
		name = (request.form.get('name') or '').strip()
		url = (request.form.get('url') or '').strip()
		kind = (request.form.get('kind') or '').strip()
		if name and url and kind in {'rss','json'}:
			s = Source(name=name, url=url, kind=kind)
			db.session.add(s)
			db.session.commit()
		return redirect(url_for('sources'))
	return render_template('sources.html', sources=Source.query.order_by(Source.created_at.desc()).all())

@app.route('/seed')
def seed():
	ensure_schema()
	added = seed_default_sources()
	return redirect(url_for('sources'))

@app.route('/ingest/<int:source_id>')
def ingest(source_id):
	ensure_schema()
	s = Source.query.get_or_404(source_id)
	added = ingest_source(s)
	return redirect(url_for('items_by_source', source_id=s.id))

@app.route('/ingest_all')
def ingest_all():
	ensure_schema()
	count = 0
	for s in Source.query.all():
		try:
			count += ingest_source(s)
		except Exception:
			pass
	return redirect(url_for('index'))

@app.route('/source/<int:source_id>')
def items_by_source(source_id):
	ensure_schema()
	s = Source.query.get_or_404(source_id)
	items = s.items.order_by(ContentItem.published_at.desc()).all()
	return render_template('items.html', items=items, sources=Source.query.all(), active_source=s.id, title=f'Source: {s.name}')

@app.route('/item/<int:item_id>')
def item_view(item_id):
	ensure_schema()
	item = ContentItem.query.get_or_404(item_id)
	data = {}
	try:
		data = json.loads(item.raw or '{}')
	except Exception:
		pass
	return render_template('item.html', item=item, data=data)

# API endpoints
@app.route('/api/sources')
def api_sources():
	ensure_schema()
	sources = Source.query.all()
	return jsonify([{'id': s.id, 'name': s.name, 'url': s.url, 'kind': s.kind} for s in sources])

@app.route('/api/content')
def api_content():
	ensure_schema()
	items = ContentItem.query.order_by(ContentItem.published_at.desc()).limit(200).all()
	return jsonify([
		{
			'id': i.id,
			'title': i.title,
			'summary': i.summary,
			'link': i.link,
			'source': i.source_id,
			'published_at': i.published_at.isoformat()
		} for i in items
	])

@app.route('/api/content/<int:item_id>')
def api_content_detail(item_id):
	ensure_schema()
	i = ContentItem.query.get_or_404(item_id)
	raw = {}
	try:
		raw = json.loads(i.raw or '{}')
	except Exception:
		pass
	return jsonify({
		'id': i.id,
		'title': i.title,
		'summary': i.summary,
		'link': i.link,
		'source': i.source_id,
		'published_at': i.published_at.isoformat(),
		'raw': raw
	})

if __name__ == '__main__':
	ensure_schema()
	seed_default_sources()
	app.run(debug=True, port=5009)
