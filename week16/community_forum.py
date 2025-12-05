import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
import json
import time
from urllib.request import urlopen
from urllib.error import URLError
import logging
from functools import wraps
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('audit')


# --- App setup ---
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.secret_key = os.getenv('W16_FORUM_SECRET', 'dev-key-change-me')
DB_PATH = os.path.join(os.path.dirname(__file__), 'community_forum.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = (os.getenv('W16_SECURE_COOKIES') or '').lower() in ('1', 'true', 'yes')
app.config['EXTERNAL_TIMEOUT_SEC'] = 4
app.config['EXTERNAL_CACHE_TTL_SEC'] = 120
app.config['RATE_LIMIT_MAX_PER_MIN'] = 20
app.config['LOGIN_MAX_FAILS'] = 5
app.config['LOGIN_LOCKOUT_MIN'] = 15
# session timeouts
app.config['SESSION_IDLE_TIMEOUT_MIN'] = int(os.getenv('W16_SESSION_IDLE_MIN', '30'))
app.config['PERMANENT_SESSION_LIFETIME'] = int(os.getenv('W16_SESSION_ABS_MIN', '1440'))  # minutes

db = SQLAlchemy(app)


# --- Models ---
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False, index=True)
	email = db.Column(db.String(120), unique=True, nullable=False, index=True)
	password_hash = db.Column(db.String(128), nullable=False)
	is_admin = db.Column(db.Boolean, default=False, nullable=False)
	bio = db.Column(db.Text)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')
	comments = db.relationship('Comment', back_populates='author', cascade='all, delete-orphan')
	sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', cascade='all, delete-orphan')
	received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient', cascade='all, delete-orphan')


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(255), nullable=False, index=True)
	body = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

	author = db.relationship('User', back_populates='posts')
	comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	body = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

	post = db.relationship('Post', back_populates='comments')
	author = db.relationship('User', back_populates='comments')


class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	body = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	read_at = db.Column(db.DateTime)

	sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
	recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='received_messages')


with app.app_context():
	db.create_all()
	# Lightweight schema migration: add missing columns if upgrading existing DB
	try:
		cols = db.session.execute(db.text("PRAGMA table_info(user)")).mappings().all()
		col_names = {row['name'] for row in cols}
		if 'is_admin' not in col_names:
			db.session.execute(db.text("ALTER TABLE user ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0"))
			db.session.commit()
		if 'bio' not in col_names:
			db.session.execute(db.text("ALTER TABLE user ADD COLUMN bio TEXT"))
			db.session.commit()
	except Exception:
		# If PRAGMA/ALTER fails, continue; user table may not exist yet or another issue.
		pass

# --- External API cache ---
_external_cache = {
	'explore_items': {
		'updated_at': 0,
		'data': []
	}
}

# shared static fallback for Explore
_EXPLORE_FALLBACK = [
	{'id': 1, 'title': 'Welcome to Explore', 'body': 'External feed is unavailable. This is a placeholder item.'},
	{'id': 2, 'title': 'Sample Post', 'body': 'Try again later to see live content.'},
]

def fetch_external_items():
	"""Fetch external items with caching and timeout, return list of dicts."""
	now = time.time()
	ttl = app.config['EXTERNAL_CACHE_TTL_SEC']
	entry = _external_cache['explore_items']
	if now - entry['updated_at'] < ttl and entry['data']:
		return entry['data']
	url = 'https://jsonplaceholder.typicode.com/posts?_limit=10'
	try:
		# urllib timeout to avoid hanging
		with urlopen(url, timeout=app.config['EXTERNAL_TIMEOUT_SEC']) as resp:
			if resp.status != 200:
				raise URLError(f'status {resp.status}')
			payload = resp.read()
			items = json.loads(payload.decode('utf-8'))
			# normalize fields
			normalized = [
				{
					'id': it.get('id'),
					'title': (it.get('title') or '').strip(),
					'body': (it.get('body') or '').strip()
				}
				for it in items
			]
			# If the external service returns an empty list, provide a static fallback
			if not normalized:
				normalized = _EXPLORE_FALLBACK
			entry['data'] = normalized
			entry['updated_at'] = now
			return normalized
	except Exception as e:
		# Log minimal error to flash; keep last cache if any
			flash('External feed unavailable.', 'error')
			if entry['data']:
				return entry['data']
			# Provide a small static fallback when cache is empty
			return _EXPLORE_FALLBACK

# --- Small helpers ---
def _paginate(query, page: int, per_page: int, order_by=None):
	"""Return (items, total, has_next, has_prev) without changing behavior."""
	total = query.count()
	if order_by is not None:
		query = query.order_by(order_by)
	items = query.offset((page - 1) * per_page).limit(per_page).all()
	has_next = page * per_page < total
	has_prev = page > 1
	return items, total, has_next, has_prev

# --- Rate limiting & lockout ---
_rate_counter = {}
_login_fails = {}

def _rate_limit(key: str, max_per_min: int = None):
	max_per_min = max_per_min or app.config['RATE_LIMIT_MAX_PER_MIN']
	now = int(time.time())
	bucket = (key, now // 60)
	_rate_counter[bucket] = _rate_counter.get(bucket, 0) + 1
	return _rate_counter[bucket] <= max_per_min

def _record_login_failure(username: str, ip: str):
	now = time.time()
	rec = _login_fails.get((username.lower(), ip))
	if rec is None:
		rec = {'fails': 1, 'locked_until': 0}
	else:
		rec['fails'] += 1
	if rec['fails'] >= app.config['LOGIN_MAX_FAILS']:
		rec['locked_until'] = now + app.config['LOGIN_LOCKOUT_MIN'] * 60
	_login_fails[(username.lower(), ip)] = rec

def _is_locked_out(username: str, ip: str):
	rec = _login_fails.get((username.lower(), ip))
	if not rec:
		return False
	if rec['locked_until'] and rec['locked_until'] > time.time():
		return True
	return False

def _reset_login_state(username: str, ip: str):
	_login_fails.pop((username.lower(), ip), None)

def _validate_password(pw: str):
	# Basic policy: length >= 8, has lower/upper/digit
	if len(pw) < 8:
		return False, 'Password must be at least 8 characters.'
	has_lower = any(c.islower() for c in pw)
	has_upper = any(c.isupper() for c in pw)
	has_digit = any(c.isdigit() for c in pw)
	if not (has_lower and has_upper and has_digit):
		return False, 'Password must include upper, lower, and a digit.'
	return True, ''


# --- Helpers ---
def current_user():
	uid = session.get('uid')
	if not uid:
		return None
	return User.query.get(uid)


def login_required(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		if not session.get('uid'):
			flash('Please log in first.', 'error')
			return redirect(url_for('login'))
		return fn(*args, **kwargs)
	return wrapper


def admin_required(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		u = current_user()
		if not u or not u.is_admin:
			flash('Admin access required.', 'error')
			return redirect(url_for('index'))
		return fn(*args, **kwargs)
	return wrapper


def author_or_admin_required(resource_author_id_getter):
	"""
	Ensure current user is resource author or admin.
	resource_author_id_getter: callable that returns the author_id for the resource.
	"""
	def decorator(fn):
		@wraps(fn)
		def wrapper(*args, **kwargs):
			u = current_user()
			if not u:
				flash('Please log in.', 'error')
				return redirect(url_for('login'))
			author_id = resource_author_id_getter(*args, **kwargs)
			if u.id != author_id and not u.is_admin:
				flash('Not authorized.', 'error')
				return redirect(url_for('index'))
			return fn(*args, **kwargs)
		return wrapper
	return decorator


@app.context_processor
def inject_user_and_csrf():
	u = current_user()
	unread = 0
	if u:
		try:
			unread = Message.query.filter_by(recipient_id=u.id, read_at=None).count()
		except Exception:
			unread = 0
	return {
		'user': u,
		'csrf_token': _csrf_token(),
		'unread_count': unread,
	}


# --- Security headers ---
@app.after_request
def add_security_headers(resp):
	csp = (
		"default-src 'self'; "
		"style-src 'self' https://cdn.jsdelivr.net; "
		"script-src 'self' https://cdn.jsdelivr.net; "
		"object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
	)
	resp.headers['Content-Security-Policy'] = csp
	resp.headers['X-Content-Type-Options'] = 'nosniff'
	resp.headers['X-Frame-Options'] = 'DENY'
	resp.headers['Referrer-Policy'] = 'no-referrer'
	return resp


# --- CSRF ---
def _csrf_token():
	tok = session.get('csrf_token')
	if not tok:
		import secrets
		tok = secrets.token_urlsafe(32)
		session['csrf_token'] = tok
	return tok


def _require_csrf():
	if app.testing:
		return True
	tok = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
	if not tok or tok != session.get('csrf_token'):
		flash('Invalid CSRF token.', 'error')
		return False
	return True


# --- Auth ---
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if not _require_csrf():
			return redirect(url_for('register'))
		# Rate-limit register per IP
		ip = request.remote_addr or 'unknown'
		if not _rate_limit(f'register:{ip}'):
			flash('Too many requests. Please try again later.', 'error')
			return redirect(url_for('register'))
		username = (request.form.get('username') or '').strip()
		email = (request.form.get('email') or '').strip()
		pw = request.form.get('password') or ''
		ok, msg = _validate_password(pw)
		if not ok:
			flash(msg, 'error')
		elif not username or not email or not pw:
			flash('All fields required.', 'error')
		elif User.query.filter(db.func.lower(User.username) == username.lower()).first():
			flash('Username already taken.', 'error')
		elif User.query.filter(db.func.lower(User.email) == email.lower()).first():
			flash('Email already in use.', 'error')
		else:
			u = User(username=username, email=email, password_hash=generate_password_hash(pw))
			db.session.add(u)
			db.session.commit()
			log.info('register success user=%s ip=%s', username, ip)
			flash('Registration successful. Please log in.', 'success')
			return redirect(url_for('login'))
	return render_template('register.html', title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if not _require_csrf():
			return redirect(url_for('login'))
		ip = request.remote_addr or 'unknown'
		username = (request.form.get('username') or '').strip()
		pw = request.form.get('password') or ''
		# Lockout check
		if _is_locked_out(username, ip):
			flash('Account temporarily locked due to failed logins. Try again later.', 'error')
			return redirect(url_for('login'))
		# Rate-limit per IP
		if not _rate_limit(f'login:{ip}'):
			flash('Too many requests. Please try again later.', 'error')
			return redirect(url_for('login'))
		u = User.query.filter(db.func.lower(User.username) == username.lower()).first()
		if not u or not check_password_hash(u.password_hash, pw):
			flash('Invalid credentials.', 'error')
			_record_login_failure(username, ip)
			log.warning('login failed user=%s ip=%s', username, ip)
		else:
			session['uid'] = u.id
			session['uname'] = u.username
			# mark session as permanent and set last activity
			session.permanent = True
			session['last_activity'] = int(time.time())
			_reset_login_state(username, ip)
			log.info('login success user=%s ip=%s', username, ip)
			flash('Logged in.', 'success')
			return redirect(url_for('index'))
	return render_template('login.html', title='Login')


@app.route('/logout')
def logout():
	session.clear()
	flash('Logged out.', 'success')
	return redirect(url_for('index'))


@app.before_request
def enforce_idle_timeout():
	uid = session.get('uid')
	if not uid:
		return
	try:
		last = int(session.get('last_activity') or 0)
	except Exception:
		last = 0
	now = int(time.time())
	idle_limit = app.config['SESSION_IDLE_TIMEOUT_MIN'] * 60
	if last and (now - last) > idle_limit:
		# idle timeout exceeded
		session.clear()
		flash('Session expired due to inactivity. Please log in again.', 'error')
		return redirect(url_for('login'))
	# update activity timestamp on each request
	session['last_activity'] = now


# --- Posts & Comments ---
@app.route('/')
def index():
	# search query
	q = (request.args.get('q') or '').strip()
	page = max(int(request.args.get('page') or 1), 1)
	per_page = 10
	query = Post.query.options(joinedload(Post.author))
	if q:
		like = f"%{q}%"
		query = query.filter(db.or_(Post.title.ilike(like), Post.body.ilike(like)))
	posts, total, has_next, has_prev = _paginate(query, page, per_page, order_by=Post.created_at.desc())
	return render_template('index.html', title='Home', posts=posts, q=q, page=page, has_next=has_next, has_prev=has_prev)


@app.route('/explore')
def explore():
	items = fetch_external_items()
	return render_template('explore.html', title='Explore', items=items)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def post_create():
	if request.method == 'POST':
		if not _require_csrf():
			return redirect(url_for('post_create'))
		title = (request.form.get('title') or '').strip()
		body = (request.form.get('body') or '').strip()
		if not title or not body:
			flash('Title and body required.', 'error')
		else:
			p = Post(author_id=session['uid'], title=title, body=body)
			db.session.add(p)
			db.session.commit()
			flash('Post created.', 'success')
			return redirect(url_for('post_view', post_id=p.id))
	return render_template('post_create.html', title='New Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_view(post_id: int):
	p = Post.query.get_or_404(post_id)
	if request.method == 'POST':
		if not session.get('uid'):
			flash('Please log in to comment.', 'error')
			return redirect(url_for('login'))
		if not _require_csrf():
			return redirect(url_for('post_view', post_id=post_id))
		body = (request.form.get('body') or '').strip()
		if not body:
			flash('Comment cannot be empty.', 'error')
		else:
			c = Comment(post_id=p.id, author_id=session['uid'], body=body)
			db.session.add(c)
			db.session.commit()
			flash('Comment added.', 'success')
			return redirect(url_for('post_view', post_id=post_id))
	# comments pagination
	cpage = max(int(request.args.get('cpage') or 1), 1)
	c_per_page = 10
	c_query = Comment.query.options(joinedload(Comment.author)).filter_by(post_id=p.id)
	comments, total_c, has_next_c, has_prev_c = _paginate(c_query, cpage, c_per_page, order_by=Comment.created_at.asc())
	return render_template('post_view.html', title=p.title, post=p, comments=comments, cpage=cpage, has_next_c=has_next_c, has_prev_c=has_prev_c)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id: int):
	p = Post.query.get_or_404(post_id)
	# authorize: author or admin
	u = current_user()
	if u.id != p.author_id and not u.is_admin:
		flash('Not authorized to delete this post.', 'error')
		return redirect(url_for('post_view', post_id=post_id))
	if not _require_csrf():
		return redirect(url_for('post_view', post_id=post_id))
	# delete post and its comments
	db.session.delete(p)
	db.session.commit()
	log.info('post delete post_id=%s by user_id=%s ip=%s', post_id, u.id, request.remote_addr)
	flash('Post deleted.', 'success')
	return redirect(url_for('index'))


# --- Messaging ---
@app.route('/messages')
@login_required
def inbox():
	msgs = Message.query.filter_by(recipient_id=session['uid']).order_by(Message.created_at.desc()).all()
	return render_template('inbox.html', title='Messages', msgs=msgs)


@app.route('/messages/compose', methods=['GET', 'POST'])
@login_required
def message_compose():
	prefill_to = (request.args.get('to') or '').strip()
	if request.method == 'POST':
		if not _require_csrf():
			return redirect(url_for('message_compose'))
		to_user = (request.form.get('to') or '').strip()
		body = (request.form.get('body') or '').strip()
		if not to_user or not body:
			flash('Recipient and message are required.', 'error')
		else:
			u = User.query.filter(db.func.lower(User.username) == to_user.lower()).first()
			if not u:
				flash('User not found.', 'error')
			else:
				m = Message(sender_id=session['uid'], recipient_id=u.id, body=body)
				db.session.add(m)
				db.session.commit()
				flash('Message sent.', 'success')
				return redirect(url_for('inbox'))
	return render_template('compose.html', title='Compose', prefill=prefill_to)


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def comment_delete(comment_id: int):
	c = Comment.query.get_or_404(comment_id)
	# authorize: comment author or admin
	u = current_user()
	if u.id != c.author_id and not u.is_admin:
		flash('Not authorized to delete this comment.', 'error')
		return redirect(url_for('post_view', post_id=c.post_id))
	if not _require_csrf():
		return redirect(url_for('post_view', post_id=c.post_id))
	db.session.delete(c)
	db.session.commit()
	log.info('comment delete comment_id=%s by user_id=%s ip=%s', comment_id, u.id, request.remote_addr)
	flash('Comment deleted.', 'success')
	return redirect(url_for('post_view', post_id=c.post_id))


# --- Profiles ---
@app.route('/user/<username>')
def user_profile(username: str):
	u = User.query.filter(db.func.lower(User.username) == (username or '').lower()).first()
	if not u:
		flash('User not found.', 'error')
		return redirect(url_for('index'))
	posts = Post.query.filter_by(author_id=u.id).order_by(Post.created_at.desc()).limit(10).all()
	return render_template('user_profile.html', title=f'{u.username} — Profile', u=u, posts=posts)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
	u = current_user()
	if request.method == 'POST':
		if not _require_csrf():
			return redirect(url_for('profile_edit'))
		bio = (request.form.get('bio') or '').strip()
		# Optional: limit bio length to avoid huge blobs
		if len(bio) > 2000:
			flash('Bio is too long (max 2000 chars).', 'error')
			return redirect(url_for('profile_edit'))
		u.bio = bio or None
		db.session.commit()
		flash('Profile updated.', 'success')
		return redirect(url_for('user_profile', username=u.username))
	return render_template('profile_edit.html', title='Edit Profile', u=u)


@app.route('/messages/<int:msg_id>')
@login_required
def message_view(msg_id: int):
	m = Message.query.get_or_404(msg_id)
	if m.recipient_id != session['uid'] and m.sender_id != session['uid']:
		flash('Not authorized.', 'error')
		return redirect(url_for('inbox'))
	# mark read if recipient
	if m.recipient_id == session['uid'] and m.read_at is None:
		m.read_at = datetime.utcnow()
		db.session.commit()
	return render_template('message.html', title='Message', m=m)


# --- Error pages ---
@app.errorhandler(404)
def not_found(e):
	return render_template('404.html', title='Not Found'), 404


@app.errorhandler(500)
def server_error(e):
	return render_template('500.html', title='Error'), 500


@app.errorhandler(401)
def unauthorized(e):
	return render_template('401.html', title='Unauthorized'), 401


@app.errorhandler(403)
def forbidden(e):
	return render_template('403.html', title='Forbidden'), 403


@app.route('/health')
def health():
	# Simple health check endpoint
	try:
		db.session.execute(db.text('SELECT 1')).scalar()
		status = 'ok'
	except Exception:
		status = 'db-error'
	return {'status': status}


if __name__ == '__main__':
	app.run(debug=True, use_reloader=False, port=int(os.getenv('PORT', '5002')))

