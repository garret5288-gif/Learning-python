# Community Forum (Week16)

A secure, feature-rich Flask community forum built as part of the Learning-python repo. It includes users, posts, comments, messaging, search, pagination, CSRF, security headers, and a polished UI with dark mode.

## Features
- User accounts with secure passwords
- Roles: admin (delete posts/comments)
- Posts: create, view, search, paginate
- Comments with pagination
- Messaging: inbox, compose, view, unread badge
- Profiles: view and edit bio (owner only)
- Explore feed via external API (cached, timeouts)
- CSRF protection across forms and POSTs
- Security headers and hardened cookies
- Rate limiting and account lockout
- Session idle timeout logout
- Bootstrap + custom CSS theme with dark mode

## Requirements
- Python 3.9+
- Flask, Flask-SQLAlchemy, Werkzeug

## Setup
1. Create/activate a virtual environment.
2. Install dependencies.
3. Run the app.

```bash
# macOS zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if present; otherwise install: flask flask-sqlalchemy werkzeug
PORT=5002 python3 Learning-python/week16/community_forum.py
```

## Configuration
Set environment variables as needed:
- `W16_FORUM_SECRET`: Flask secret key
- `W16_SECURE_COOKIES`: 1/true to enable Secure cookies
- `W16_SESSION_IDLE_MIN`: minutes before idle logout (default 30)
- `W16_SESSION_ABS_MIN`: absolute session lifetime minutes (default 1440)
- `EXTERNAL_TIMEOUT_SEC`: external fetch timeout (default 4)
- `EXTERNAL_CACHE_TTL_SEC`: external feed cache TTL (default 120)
- `PORT`: app port (default 5002)

## How to use
- Register and login.
- Create posts, search with the top search bar.
- View a post and add comments; use pagination for long threads.
- Visit profiles (`/user/<username>`). If it's yours, click Edit Profile to update bio.
- Check Messages for inbox, compose, and open message view.
- Try Explore for external feed items.
- Toggle dark mode from the navbar; it persists via localStorage.

## Routes (selected)
- `/` Home: posts index (search, pagination)
- `/register`, `/login`, `/logout`
- `/post/create`, `/post/<id>`
- `/post/<id>/delete` (author or admin)
- `/comment/<id>/delete` (author or admin)
- `/messages`, `/messages/compose`, `/messages/<id>`
- `/user/<username>` profile
- `/profile/edit` edit your bio
- `/explore` external feed

## Security notes
- CSRF token required for POST (skipped only in testing mode).
- Content Security Policy blocks inline scripts; theme JS is loaded from `static/theme.js`.
- Cookies: HttpOnly, SameSite=Lax; Secure configurable.
- Rate limiting per IP and login lockout after repeated failures.
- Password policy enforced on registration.
- Session idle timeout enforced; absolute lifetime configurable.

## Troubleshooting
- Port in use: change `PORT` or kill the other process.
- SQLite schema errors after updates: the app runs a lightweight migration (ALTER TABLE) for new columns like `is_admin` and `bio`.
- BuildError on author links: templates guard missing usernames.
- Dark mode issues: ensure `static/app.css` and `static/theme.js` are loaded; CSP disallows inline JS.

## Week15 app (older)
An earlier forum with moderation; templates under `Learning-python/week15/day5/forum_templates/`. It uses a separate DB and model set.

---

## License
Educational use. No warranty.
