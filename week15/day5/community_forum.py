import os
import time
import secrets
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'forum.db')


def simple_hash(pw: str) -> str:
    """Deprecated: kept for backward compatibility if existing data uses it."""
    salt = 'slt'
    h = 0x811C9DC5
    for ch in (salt + pw):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def login_required(fn):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    # Preserve original function metadata to avoid Flask endpoint collisions
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    wrapper.__module__ = fn.__module__
    return wrapper


def moderator_required(fn):
    def wrapper(*args, **kwargs):
        if not session.get('is_moderator'):
            flash('Moderator access required.', 'error')
            return redirect(url_for('index'))
        return fn(*args, **kwargs)
    # Preserve original function metadata to avoid Flask endpoint collisions
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    wrapper.__module__ = fn.__module__
    return wrapper


app = Flask(__name__, template_folder='forum_templates', static_folder='static')
# Use a strong secret key from environment or generate a random fallback (development only)
app.secret_key = os.getenv('FORUM_SECRET_KEY', secrets.token_hex(32))
# Cookie hardening (configurable). Default off in debug for local HTTP.
_secure_cookies_env = os.getenv('FORUM_SECURE_COOKIES')
if _secure_cookies_env is not None:
    app.config['SESSION_COOKIE_SECURE'] = _secure_cookies_env.strip() in ('1', 'true', 'True')
else:
    app.config['SESSION_COOKIE_SECURE'] = not app.debug  # on in prod, off in debug
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Cap request size (e.g., 2 MB)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Session inactivity timeout (seconds). Default 20 minutes. Override with env FORUM_IDLE_TIMEOUT.
IDLE_TIMEOUT_SECONDS = int(os.getenv('FORUM_IDLE_TIMEOUT', '1200'))

# --- MODELS ---
class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_moderator = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='author', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)
    author = db.relationship('Account', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

    @property
    def comment_count(self) -> int:
        return sum(1 for c in self.comments if not c.is_deleted)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime)
    post = db.relationship('Post', back_populates='comments')
    author = db.relationship('Account', back_populates='comments')


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    reporter_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(32), default='open', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Helpful relationships for templates
    post = db.relationship('Post', primaryjoin='Report.post_id == Post.id', lazy='joined')
    comment = db.relationship('Comment', primaryjoin='Report.comment_id == Comment.id', lazy='joined')

# --- HELPERS ---
def ensure_schema():
    # Create tables if they do not exist
    with app.app_context():
        db.create_all()

# Initialize DB once at import time
ensure_schema()


def current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    return Account.query.get(uid)


@app.context_processor
def inject_user():
    # Make common values available to all templates
    return {
        'user': current_user(),
        'current_year': datetime.now(UTC).year,
        'csrf_token': get_csrf_token(),
    }


@app.template_filter('dt')
def format_datetime(value):
    """Format a datetime for display."""
    if not value:
        return ''
    try:
        # Convert to US Eastern time. Assume naive datetimes are UTC.
        et = ZoneInfo('America/New_York')
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=ZoneInfo('UTC'))
            value = value.astimezone(et)
        return value.strftime('%b %d, %Y %I:%M %p')
    except Exception:
        return str(value)


@app.before_request
def enforce_session_timeout():
    # Skip checks for static assets
    if not session.get('user_id'):
        return None
    try:
        last = float(session.get('last_activity', 0))
    except Exception:
        last = 0.0
    now = time.time()
    if last and IDLE_TIMEOUT_SECONDS > 0 and (now - last) > IDLE_TIMEOUT_SECONDS:
        # Inactive for too long: clear session and force re-login
        session.clear()
        flash('You were logged out due to inactivity.', 'error')
        return redirect(url_for('login'))
    # Refresh activity timestamp for sliding expiration
    session['last_activity'] = now
    return None


# --- Monitoring & Logging ---
# Configure application logger with rotating file handler and console output
logger = logging.getLogger('community_forum')
logger.setLevel(logging.INFO)
_fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
_fh = RotatingFileHandler('community_forum.log', maxBytes=1024*1024, backupCount=5)
_fh.setFormatter(_fmt)
_ch = logging.StreamHandler()
_ch.setFormatter(_fmt)
if not logger.handlers:
    logger.addHandler(_fh)
    logger.addHandler(_ch)


@app.before_request
def start_request_timer():
    # Mark start time and basic request info for monitoring
    session['_rt_start'] = time.time()


@app.after_request
def log_request(resp):
    try:
        start = float(session.get('_rt_start', 0))
        dur_ms = int((time.time() - start) * 1000) if start else -1
    except Exception:
        dur_ms = -1
    user = session.get('username') or '-'
    logger.info('req method=%s path=%s status=%s user=%s dur_ms=%s', request.method, request.path, resp.status_code, user, dur_ms)
    return resp


@app.errorhandler(Exception)
def log_unhandled_error(e):
    # Log unexpected exceptions; rely on Flask's default error handling to render response
    logger.exception('Unhandled error: %s', e)
    return make_response(render_template('base.html', title='Server Error'), 500)


# --- Security Headers ---
@app.after_request
def add_security_headers(resp):
    # CSP: allow self-hosted assets and Bootstrap CDN; disallow inline scripts; tighten frames and objects
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

# --- Debug helpers ---
@app.route('/__session')
def debug_session():
    """Show current session keys for debugging. Only enabled in debug mode."""
    if not app.debug:
        return make_response('Not available', 404)
    data = {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'is_moderator': session.get('is_moderator'),
        'last_activity': session.get('last_activity'),
    }
    return data

@app.route('/__make_test_user')
def make_test_user():
    """Create a test user and log them in (debug only)."""
    if not app.debug:
        return make_response('Not available', 404)
    username = request.args.get('u', 'testuser')
    email = f"{username}@example.com"
    pw = 'Password123'
    acc = Account.query.filter(db.func.lower(Account.username) == username.lower()).first()
    if not acc:
        is_first_user = db.session.query(db.func.count(Account.id)).scalar() == 0
        acc = Account(
            username=username,
            email=email,
            password_hash=generate_password_hash(pw, method='pbkdf2:sha256', salt_length=16),
            is_moderator=is_first_user,
        )
        db.session.add(acc)
        db.session.commit()
    session['user_id'] = acc.id
    session['username'] = acc.username
    session['is_moderator'] = 1 if acc.is_moderator else 0
    session['last_activity'] = time.time()
    return {'status': 'ok', 'user': acc.username}


# --- CSRF ---
def get_csrf_token() -> str:
    token = session.get('csrf_token')
    if not token:
        token = secrets.token_urlsafe(32)
        session['csrf_token'] = token
    return token


def require_csrf():
    # Skip CSRF in debug or testing mode to ease local development and allow unit tests
    if app.debug or app.testing:
        return True
    token_form = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
    if not token_form or token_form != session.get('csrf_token'):
        flash('Invalid CSRF token.', 'error')
        return False
    return True


# --- Auth ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if not require_csrf():
            return redirect(url_for('register'))
        username = (request.form.get('username') or '').strip()
        email = (request.form.get('email') or '').strip()
        pw = request.form.get('password') or ''
        pw2 = request.form.get('confirm_password') or ''
        if not username or not email or not pw:
            flash('All fields are required.', 'error')
        elif pw != pw2:
            flash('Passwords do not match.', 'error')
        else:
            if Account.query.filter(db.func.lower(Account.username) == username.lower()).first() or \
               Account.query.filter(db.func.lower(Account.email) == email.lower()).first():
                flash('Username or email already in use.', 'error')
            else:
                # If this is the first account, make it a moderator
                is_first_user = db.session.query(db.func.count(Account.id)).scalar() == 0
                acc = Account(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(pw, method='pbkdf2:sha256', salt_length=16),
                    is_moderator=is_first_user,
                )
                db.session.add(acc)
                db.session.commit()
                if is_first_user:
                    flash('First user detected: moderator privileges granted.', 'success')
                flash('Registration successful. Please login.', 'success')
                return redirect(url_for('login'))
    return render_template('register.html', csrf_token=get_csrf_token())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not require_csrf():
            return redirect(url_for('login'))
        username = (request.form.get('username') or '').strip()
        pw = request.form.get('password') or ''
        acc = Account.query.filter(db.func.lower(Account.username) == username.lower()).first()
        # Support legacy simple_hash for existing users, but prefer PBKDF2
        valid = False
        if acc:
            try:
                valid = check_password_hash(acc.password_hash, pw)
            except Exception:
                # if stored hash is legacy simple_hash
                valid = (simple_hash(pw) == acc.password_hash)
        if not acc or not valid:
            flash('Invalid credentials.', 'error')
        else:
            session['user_id'] = acc.id
            session['username'] = acc.username
            session['is_moderator'] = 1 if acc.is_moderator else 0
            acc.last_login = datetime.now(UTC)
            db.session.commit()
            flash('Logged in.', 'success')
            return redirect(url_for('index'))
    return render_template('login.html', csrf_token=get_csrf_token())


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'success')
    return redirect(url_for('index'))


# --- Posts & Comments ---

@app.route('/')
def index():
    posts = Post.query.filter_by(is_deleted=False).order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/post/create', methods=['GET', 'POST'])
@login_required
def post_create():
    if request.method == 'POST':
        if not require_csrf():
            return redirect(url_for('post_create'))
        title = (request.form.get('title') or '').strip()
        body = (request.form.get('body') or '').strip()
        if not title or not body:
            flash('Title and body are required.', 'error')
        else:
            post = Post(
                author_id=session['user_id'],
                title=title,
                body=body,
            )
            db.session.add(post)
            db.session.commit()
            flash('Post created.', 'success')
            return redirect(url_for('post_view', post_id=post.id))
    return render_template('post_form.html', mode='create', csrf_token=get_csrf_token())


def can_edit_post(post):
    u = current_user()
    return bool(u and (u.is_moderator or u.id == post.author_id))


@app.route('/post/<int:post_id>')
def post_view(post_id: int):
    p = Post.query.get(post_id)
    if not p or p.is_deleted:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))
    comments = [c for c in p.comments if not c.is_deleted]
    comments.sort(key=lambda c: c.created_at)
    return render_template('post_view.html', post=p, comments=comments, can_edit=can_edit_post(p))


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(post_id: int):
    p = Post.query.get(post_id)
    if not p or p.is_deleted:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))
    if not can_edit_post(p):
        flash('You can only edit your own posts.', 'error')
        return redirect(url_for('post_view', post_id=post_id))
    if request.method == 'POST':
        if not require_csrf():
            return render_template('post_form.html', mode='edit', post=p)
        title = (request.form.get('title') or '').strip()
        body = (request.form.get('body') or '').strip()
        if not title or not body:
            flash('Title and body are required.', 'error')
            return render_template('post_form.html', mode='edit', post=p)
        p.title = title
        p.body = body
    p.updated_at = datetime.now(UTC)
    db.session.commit()
    flash('Post updated.', 'success')
    return redirect(url_for('post_view', post_id=post_id))
    return render_template('post_form.html', mode='edit', post=p, csrf_token=get_csrf_token())


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def post_delete(post_id: int):
    if not require_csrf():
        return redirect(url_for('post_view', post_id=post_id))
    p = Post.query.get(post_id)
    if not p:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))
    if not can_edit_post(p):
        flash('You can only delete your own posts.', 'error')
        return redirect(url_for('post_view', post_id=post_id))
    p.is_deleted = True
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>/lock', methods=['POST'])
@login_required
def post_lock(post_id: int):
    if not require_csrf():
        return redirect(url_for('post_view', post_id=post_id))
    if not session.get('is_moderator'):
        flash('Moderator access required.', 'error')
        return redirect(url_for('post_view', post_id=post_id))
    p = Post.query.get(post_id)
    if not p:
        flash('Post not found.', 'error')
    else:
        p.is_locked = not bool(p.is_locked)
        db.session.commit()
        flash('Post locked.' if p.is_locked else 'Post unlocked.', 'success')
    return redirect(url_for('post_view', post_id=post_id))


@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_add(post_id: int):
    if not require_csrf():
        return redirect(url_for('post_view', post_id=post_id))
    body = (request.form.get('body') or '').strip()
    if not body:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('post_view', post_id=post_id))
    p = Post.query.get(post_id)
    if not p or p.is_deleted:
        flash('Post not found.', 'error')
        return redirect(url_for('index'))
    if p.is_locked:
        flash('Post is locked. Comments are disabled.', 'error')
        return redirect(url_for('post_view', post_id=post_id))
    cmt = Comment(post_id=post_id, author_id=session['user_id'], body=body)
    db.session.add(cmt)
    db.session.commit()
    flash('Comment added.', 'success')
    return redirect(url_for('post_view', post_id=post_id))


@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def comment_delete(comment_id: int):
    if not require_csrf():
        c = Comment.query.get(comment_id)
        return redirect(url_for('post_view', post_id=(c.post_id if c else 0)))
    c = Comment.query.get(comment_id)
    if not c:
        flash('Comment not found.', 'error')
        return redirect(url_for('index'))
    if not (session.get('is_moderator') or session.get('user_id') == c.author_id):
        flash('You can only delete your own comments.', 'error')
        return redirect(url_for('post_view', post_id=c.post_id))
    c.is_deleted = True
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect(url_for('post_view', post_id=c.post_id))


# --- Reporting & Moderation ---

@app.route('/post/<int:post_id>/report', methods=['POST'])
@login_required
def report_post(post_id: int):
    if not require_csrf():
        return redirect(url_for('post_view', post_id=post_id))
    reason = (request.form.get('reason') or '').strip() or 'No reason provided'
    rpt = Report(post_id=post_id, reporter_id=session['user_id'], reason=reason)
    db.session.add(rpt)
    db.session.commit()
    flash('Post reported.', 'success')
    return redirect(url_for('post_view', post_id=post_id))


@app.route('/comment/<int:comment_id>/report', methods=['POST'])
@login_required
def report_comment(comment_id: int):
    if not require_csrf():
        return redirect(url_for('post_view', post_id=comment_id))
    reason = (request.form.get('reason') or '').strip() or 'No reason provided'
    c = Comment.query.get(comment_id)
    if not c:
        flash('Comment not found.', 'error')
        return redirect(url_for('index'))
    rpt = Report(comment_id=comment_id, reporter_id=session['user_id'], reason=reason)
    db.session.add(rpt)
    db.session.commit()
    flash('Comment reported.', 'success')
    return redirect(url_for('post_view', post_id=c.post_id))


@app.route('/moderation')
@login_required
@moderator_required
def moderation():
    reports = Report.query.filter_by(status='open').order_by(Report.created_at.desc()).all()
    deleted_posts = Post.query.filter_by(is_deleted=True).order_by(Post.id.desc()).all()
    deleted_comments = Comment.query.filter_by(is_deleted=True).order_by(Comment.id.desc()).all()
    return render_template('moderation.html', reports=reports, deleted_posts=deleted_posts, deleted_comments=deleted_comments)


@app.route('/reports/<int:report_id>/resolve', methods=['POST'])
@login_required
@moderator_required
def resolve_report(report_id: int):
    if not require_csrf():
        return redirect(url_for('moderation'))
    rpt = Report.query.get(report_id)
    if rpt:
        rpt.status = 'resolved'
        db.session.commit()
    flash('Report resolved.', 'success')
    return redirect(url_for('moderation'))


@app.route('/moderation/restore/post/<int:post_id>', methods=['POST'])
@login_required
@moderator_required
def restore_post(post_id: int):
    if not require_csrf():
        return redirect(url_for('moderation'))
    p = Post.query.get(post_id)
    if p:
        p.is_deleted = False
        db.session.commit()
    flash('Post restored.', 'success')
    return redirect(url_for('moderation'))


@app.route('/moderation/restore/comment/<int:comment_id>', methods=['POST'])
@login_required
@moderator_required
def restore_comment(comment_id: int):
    if not require_csrf():
        return redirect(url_for('moderation'))
    c = Comment.query.get(comment_id)
    if c:
        c.is_deleted = False
        db.session.commit()
    flash('Comment restored.', 'success')
    return redirect(url_for('moderation'))

if __name__ == '__main__':
    # Disable the auto-reloader to avoid multiple processes with different secret keys in debug
    app.run(debug=True, use_reloader=False, port=int(os.getenv('PORT', '5000')))