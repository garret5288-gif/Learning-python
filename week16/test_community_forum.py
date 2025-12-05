import os
import tempfile
import unittest
import sys
import importlib.util

# Dynamically load the week16 app module by file path to avoid package name issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PATH = os.path.join(BASE_DIR, 'community_forum.py')
spec = importlib.util.spec_from_file_location("week16_app", APP_PATH)
week16_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(week16_app)

app = week16_app.app
db = week16_app.db
User = week16_app.User
Post = week16_app.Post
Comment = week16_app.Comment
Message = week16_app.Message


class ForumTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        # Temporary SQLite DB per test run
        self.db_fd, self.db_path = tempfile.mkstemp(prefix='w16_test_', suffix='.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        # Push app context for the duration of the test case
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        try:
            # Cleanup session and dispose engine to close DB connections
            db.session.remove()
            try:
                db.get_engine(app).dispose()
            except Exception:
                try:
                    db.engine.dispose()
                except Exception:
                    pass
            # Pop app context
            try:
                self.app_ctx.pop()
            except Exception:
                pass
            os.close(self.db_fd)
            os.unlink(self.db_path)
        except Exception:
            pass


    def register_and_login(self, username='alice', email='a@example.com', password='Password1'):
    # Register
        rv = self.client.post('/register', data={
        'username': username,
        'email': email,
        'password': password,
        'csrf_token': 'x',  # CSRF skipped in testing
    }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
    # Login
        rv = self.client.post('/login', data={
        'username': username,
        'password': password,
        'csrf_token': 'x',
    }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)


    def test_home_page(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Latest posts', rv.data)


    def test_register_login_create_post_comment(self):
        self.register_and_login()
    # Create post
        rv = self.client.post('/post/create', data={
        'title': 'Hello',
        'body': 'World',
        'csrf_token': 'x',
    }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Hello', rv.data)
    # Add comment
        rv = self.client.post('/post/1', data={
        'body': 'Nice post',
        'csrf_token': 'x',
    }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Nice post', rv.data)


    def test_profile_view_and_edit_bio(self):
        self.register_and_login()
    # View profile
        rv = self.client.get('/user/alice')
        self.assertEqual(rv.status_code, 200)
    # Edit bio
        rv = self.client.post('/profile/edit', data={
        'bio': 'I love coding.',
        'csrf_token': 'x',
    }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'I love coding.', rv.data)


    def test_messaging_flow(self):
        # Create two users
        self.register_and_login(username='alice', email='a@example.com')
        self.client.get('/logout')
        self.register_and_login(username='bob', email='b@example.com')
        # Bob sends message to Alice
        rv = self.client.post('/messages/compose', data={
            'to': 'alice',
            'body': 'Hi Alice',
            'csrf_token': 'x',
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        # Check inbox for Bob (should not contain the message)
        rv = self.client.get('/messages')
        self.assertNotIn(b'Hi Alice', rv.data)
        # Logout Bob, login Alice
        self.client.get('/logout')
        rv = self.client.post('/login', data={
            'username': 'alice',
            'password': 'Password1',
            'csrf_token': 'x',
        }, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        # Alice sees message in inbox and on message detail page
        rv = self.client.get('/messages')
        self.assertEqual(rv.status_code, 200)
        # Open the first message (id 1 in this isolated test DB)
        rv = self.client.get('/messages/1')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Hi Alice', rv.data)


    def test_explore_works(self):
    # External fetch may fail; page should still render
        rv = self.client.get('/explore')
        self.assertEqual(rv.status_code, 200)


    def test_delete_post_authorization(self):
        self.register_and_login(username='alice', email='a@example.com')
        self.client.post('/post/create', data={'title': 't', 'body': 'b', 'csrf_token': 'x'}, follow_redirects=True)
        self.client.get('/logout')
        self.register_and_login(username='bob', email='b@example.com')
    # Bob cannot delete Alice's post
        rv = self.client.post('/post/1/delete', data={'csrf_token': 'x'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(b'Not authorized' in rv.data or b'Not authorized to delete' in rv.data)


    def test_health_endpoint(self):
        rv = self.client.get('/health')
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(rv.is_json)
        self.assertIn(rv.json.get('status'), ('ok', 'db-error'))


if __name__ == '__main__':
    unittest.main()
