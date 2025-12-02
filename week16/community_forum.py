import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# --- App setup ---
app = Flask(__name__)
app.secret_key = os.getenv('W16_FORUM_SECRET', 'dev-key-change-me')
DB_PATH = os.path.join(os.path.dirname(__file__), 'community_forum.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = (os.getenv('W16_SECURE_COOKIES') or '').lower() in ('1', 'true', 'yes')

db = SQLAlchemy(app)


# --- Models ---
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')
	comments = db.relationship('Comment', back_populates='author', cascade='all, delete-orphan')
	sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', cascade='all, delete-orphan')
	received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient', cascade='all, delete-orphan')


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(255), nullable=False)
	body = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	author = db.relationship('User', back_populates='posts')
	comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	body = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

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


# --- Helpers ---
def current_user():
	uid = session.get('uid')
	if not uid:
		return None
	return User.query.get(uid)


def login_required(fn):
	def wrapper(*args, **kwargs):
		if not session.get('uid'):
			flash('Please log in first.', 'error')
			return redirect(url_for('login'))
		return fn(*args, **kwargs)
	wrapper.__name__ = fn.__name__
	return wrapper


@app.context_processor
def inject_user_and_csrf():
	return {
		'user': current_user(),
		'csrf_token': _csrf_token(),
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
		username = (request.form.get('username') or '').strip()
		email = (request.form.get('email') or '').strip()
		pw = request.form.get('password') or ''
		if not username or not email or not pw:
			flash('All fields required.', 'error')
		elif User.query.filter(db.func.lower(User.username) == username.lower()).first():
			flash('Username already taken.', 'error')
		elif User.query.filter(db.func.lower(User.email) == email.lower()).first():
			flash('Email already in use.', 'error')
		else:
			u = User(username=username, email=email, password_hash=generate_password_hash(pw))
			db.session.add(u)
			db.session.commit()
			flash('Registration successful. Please log in.', 'success')
			return redirect(url_for('login'))
	return render_template('register.html', title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if not _require_csrf():
			return redirect(url_for('login'))
		username = (request.form.get('username') or '').strip()
		pw = request.form.get('password') or ''
		u = User.query.filter(db.func.lower(User.username) == username.lower()).first()
		if not u or not check_password_hash(u.password_hash, pw):
			flash('Invalid credentials.', 'error')
		else:
			session['uid'] = u.id
			session['uname'] = u.username
			flash('Logged in.', 'success')
			return redirect(url_for('index'))
	return render_template('login.html', title='Login')


@app.route('/logout')
def logout():
	session.clear()
	flash('Logged out.', 'success')
	return redirect(url_for('index'))


# --- Posts & Comments ---
@app.route('/')
def index():
	posts = Post.query.order_by(Post.created_at.desc()).all()
	return render_template('index.html', title='Home', posts=posts)


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
	comments = Comment.query.filter_by(post_id=p.id).order_by(Comment.created_at.asc()).all()
	return render_template('post_view.html', title=p.title, post=p, comments=comments)


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


# --- Profiles ---
@app.route('/user/<username>')
def user_profile(username: str):
	u = User.query.filter(db.func.lower(User.username) == (username or '').lower()).first()
	if not u:
		flash('User not found.', 'error')
		return redirect(url_for('index'))
	posts = Post.query.filter_by(author_id=u.id).order_by(Post.created_at.desc()).limit(10).all()
	return render_template('user_profile.html', title=f'{u.username} — Profile', u=u, posts=posts)


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


if __name__ == '__main__':
	app.run(debug=True, use_reloader=False, port=int(os.getenv('PORT', '5002')))

