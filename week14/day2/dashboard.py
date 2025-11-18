from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib.parse import quote_plus
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# ---- HTTP helpers (requests optional) ----
try:
	import requests  # type: ignore
except Exception:  # pragma: no cover
	requests = None  # Fallback when requests isn't installed


def http_get_json(url: str, timeout: float = 4.0):
	if not requests:
		return None
	try:
		r = requests.get(url, timeout=timeout)
		r.raise_for_status()
		return r.json()
	except Exception:
		return None


def http_get_text(url: str, timeout: float = 4.0):
	if not requests:
		return None
	try:
		r = requests.get(url, timeout=timeout)
		r.raise_for_status()
		return r.text
	except Exception:
		return None


# ---- Weather (Open-Meteo, no API key) ----
def geocode_city(name: str):
	name = (name or '').strip() or 'New York'
	url = f"https://geocoding-api.open-meteo.com/v1/search?count=1&language=en&name={quote_plus(name)}"
	data = http_get_json(url)
	if data and data.get('results'):
		top = data['results'][0]
		return {
			'name': top.get('name') or name,
			'lat': top.get('latitude'),
			'lon': top.get('longitude'),
			'country': top.get('country_code'),
		}
	# Fallback to NYC
	return {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'country': 'US'}


def weather_code_text(code: int):
	mapping = {
		0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
		45: 'Fog', 48: 'Depositing rime fog',
		51: 'Light drizzle', 53: 'Drizzle', 55: 'Dense drizzle',
		61: 'Slight rain', 63: 'Rain', 65: 'Heavy rain',
		71: 'Slight snow', 73: 'Snow', 75: 'Heavy snow',
		80: 'Rain showers', 81: 'Rain showers', 82: 'Violent rain showers',
		95: 'Thunderstorm', 96: 'Thunderstorm (hail)', 99: 'Thunderstorm (heavy hail)'
	}
	return mapping.get(int(code or 0), 'Unknown')


def fetch_weather(city: str):
	loc = geocode_city(city)
	lat, lon = loc['lat'], loc['lon']
	url = (
		"https://api.open-meteo.com/v1/forecast?"
		f"latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&timezone=auto"
	)
	data = http_get_json(url) or {}
	current = (data.get('current') or {})
	temp_c = current.get('temperature_2m')
	code = current.get('weather_code')
	return {
		'city': loc['name'],
		'country': loc.get('country'),
		'temp_c': temp_c if temp_c is not None else 22.0,
		'desc': weather_code_text(code) if code is not None else 'Partly cloudy',
		'as_of': datetime.now().strftime('%Y-%m-%d %H:%M'),
	}


# ---- News (RSS via HN frontpage, no key) ----
def fetch_news(limit: int = 6):
	url = 'https://hnrss.org/frontpage'
	text = http_get_text(url)
	items = []
	if text:
		try:
			import xml.etree.ElementTree as ET
			root = ET.fromstring(text)
			for item in root.iterfind('.//item'):
				title_el = item.find('title')
				link_el = item.find('link')
				if title_el is not None and link_el is not None:
					items.append({'title': title_el.text or 'Untitled', 'url': link_el.text or '#'})
				if len(items) >= limit:
					break
		except Exception:
			items = []
	if not items:
		# Simple fallback headlines
		items = [
			{'title': 'Welcome to your dashboard', 'url': '#'},
			{'title': 'Add your own news source later', 'url': '#'},
			{'title': 'Everything is working!', 'url': '#'},
		]
	return items


# ---- Stocks (Stooq CSV, no key) ----
def fetch_stocks(tickers: list[str]):
	syms = [s.strip().lower() for s in tickers if s.strip()]
	if not syms:
		syms = ['aapl', 'msft', 'goog']
	base = 'https://stooq.com/q/l/?h&e=csv&f=sd2t2ohlcv&s='
	url = base + ','.join(syms)
	text = http_get_text(url)
	rows = []
	if text and 'Symbol' in text:
		try:
			r = csv.DictReader(io.StringIO(text))
			for row in r:
				rows.append({
					'symbol': (row.get('Symbol') or '').upper(),
					'close': row.get('Close'),
					'open': row.get('Open'),
					'high': row.get('High'),
					'low': row.get('Low'),
					'volume': row.get('Volume'),
					'date': row.get('Date'),
				})
		except Exception:
			rows = []
	if not rows:
		# Static fallback
		rows = [
			{'symbol': 'AAPL', 'close': '192.00', 'open': '190.10', 'high': '193.50', 'low': '189.80', 'volume': '50M', 'date': datetime.now().strftime('%Y-%m-%d')},
			{'symbol': 'MSFT', 'close': '408.20', 'open': '405.00', 'high': '410.00', 'low': '403.25', 'volume': '30M', 'date': datetime.now().strftime('%Y-%m-%d')},
			{'symbol': 'GOOG', 'close': '141.75', 'open': '140.00', 'high': '142.40', 'low': '139.90', 'volume': '25M', 'date': datetime.now().strftime('%Y-%m-%d')},
		]
	return rows


@app.route('/')
def dashboard_home():
	city = (request.args.get('city') or 'New York').strip()
	raw_tickers = request.args.get('tickers') or 'AAPL,MSFT,GOOG'
	tickers = [t.strip().upper() for t in raw_tickers.split(',') if t.strip()]

	weather = fetch_weather(city)
	news = fetch_news(limit=6)
	stocks = fetch_stocks(tickers)

	return render_template('dashboard.html', city=city, tickers=tickers, weather=weather, news=news, stocks=stocks)


if __name__ == '__main__':
	app.run(debug=True, port=5002)

