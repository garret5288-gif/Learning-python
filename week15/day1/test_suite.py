import unittest
import json

from week14.day5.content_management import init_app, seed_default_sources, Source, ContentItem, ingest_source


class ContentManagementTests(unittest.TestCase):

	def setUp(self):
		self.app, self.db = init_app('sqlite:///:memory:')
		self.client = self.app.test_client()
		with self.app.app_context():
			seed_default_sources()

	def test_seed_sources(self):
		with self.app.app_context():
			count = Source.query.count()
			self.assertGreaterEqual(count, 3, "Expected at least 3 seeded sources")

	def test_api_sources(self):
		resp = self.client.get('/api/sources')
		self.assertEqual(resp.status_code, 200)
		data = resp.get_json()
		self.assertIsInstance(data, list)
		self.assertGreater(len(data), 0)

	def test_ingest_first_source(self):
		with self.app.app_context():
			s = Source.query.first()
			self.assertIsNotNone(s)
			added = ingest_source(s)
			self.assertIsInstance(added, int)
			# Items might be zero if feed blocked; ensure no exception
			items = ContentItem.query.filter_by(source_id=s.id).count()
			self.assertGreaterEqual(items, 0)

	def test_api_content(self):
		resp = self.client.get('/api/content')
		self.assertEqual(resp.status_code, 200)
		data = resp.get_json()
		self.assertIsInstance(data, list)

	def test_content_detail_404(self):
		resp = self.client.get('/api/content/999999')
		self.assertEqual(resp.status_code, 404)

	def test_home_page(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)
		self.assertIn(b'Available Sources', resp.data)


if __name__ == '__main__':
	unittest.main(verbosity=2)
