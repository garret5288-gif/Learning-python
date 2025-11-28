import os
import tempfile
import unittest
from datetime import datetime

from week15.day5.community_forum import app, db, Account, Post, Comment, Report


class CommunityForumTests(unittest.TestCase):
    def setUp(self):
        # Use a temporary DB file per test run
        self.tmpdir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.tmpdir.name, 'test_forum.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['TESTING'] = True
        self.app = app
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()

    def register(self, username='alice', email='alice@example.com', pw='Password123'):
        return self.client.post('/register', data={
            'username': username,
            'email': email,
            'password': pw,
            'confirm_password': pw,
        }, follow_redirects=True)

    def login(self, username='alice', pw='Password123'):
        return self.client.post('/login', data={
            'username': username,
            'password': pw,
        }, follow_redirects=True)

    def test_register_and_login(self):
        rv = self.register()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Registration successful', rv.data)
        rv = self.login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Logged in.', rv.data)

    def test_create_post_and_view(self):
        self.register()
        self.login()
        rv = self.client.post('/post/create', data={'title': 'Hello', 'body': 'World'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Post created', rv.data)
        # Index shows post
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Hello', rv.data)

    def test_comment_add_and_delete(self):
        self.register()
        self.login()
        # Create post
        self.client.post('/post/create', data={'title': 'Topic', 'body': 'Body'}, follow_redirects=True)
        with self.app.app_context():
            post = Post.query.first()
            self.assertIsNotNone(post)
            pid = post.id
        # Add comment
        rv = self.client.post(f'/post/{pid}/comment', data={'body': 'Nice!'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Comment added', rv.data)
        with self.app.app_context():
            c = Comment.query.filter_by(post_id=pid).first()
            self.assertIsNotNone(c)
            cid = c.id
        # Delete comment
        rv = self.client.post(f'/comment/{cid}/delete', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Comment deleted', rv.data)

    def test_lock_post_prevents_comments(self):
        # Make moderator (first user)
        self.register('mod', 'mod@example.com')
        self.login('mod')
        # Create post
        self.client.post('/post/create', data={'title': 'Locked', 'body': 'Body'}, follow_redirects=True)
        with self.app.app_context():
            post = Post.query.first()
            pid = post.id
        # Lock
        rv = self.client.post(f'/post/{pid}/lock', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Post locked', rv.data)
        # Try comment
        rv = self.client.post(f'/post/{pid}/comment', data={'body': 'Can I?'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Post is locked', rv.data)

    def test_report_and_moderation(self):
        # Moderator
        self.register('mod', 'mod@example.com')
        self.login('mod')
        # User
        self.register('bob', 'bob@example.com')
        self.login('bob')
        # Bob creates post
        self.client.post('/post/create', data={'title': 'Report me', 'body': 'Body'}, follow_redirects=True)
        with self.app.app_context():
            post = Post.query.first()
            pid = post.id
        # Bob reports post
        rv = self.client.post(f'/post/{pid}/report', data={'reason': 'Spam'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Post reported', rv.data)
        # Moderator resolves report
        self.login('mod')
        with self.app.app_context():
            rpt = Report.query.first()
            self.assertIsNotNone(rpt)
            rid = rpt.id
        rv = self.client.post(f'/reports/{rid}/resolve', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Report resolved', rv.data)

    def test_delete_and_restore_post(self):
        # Moderator
        self.register('mod', 'mod@example.com')
        self.login('mod')
        # Create post
        self.client.post('/post/create', data={'title': 'ToDelete', 'body': 'Body'}, follow_redirects=True)
        with self.app.app_context():
            post = Post.query.first()
            pid = post.id
        # Delete
        rv = self.client.post(f'/post/{pid}/delete', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Post deleted', rv.data)
        # Restore via moderation
        rv = self.client.get('/moderation', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        rv = self.client.post(f'/moderation/restore/post/{pid}', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Post restored', rv.data)

    def test_auth_required_redirects(self):
        # Access create post without login
        rv = self.client.get('/post/create', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Please login first', rv.data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
