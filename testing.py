import unittest
from unittest.mock import patch
from app import app, connect_db
class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"", response.data)
    def test_connect_db(self):
        conn = connect_db()
        self.assertIsNotNone(conn)
if __name__ == '__main__':
    unittest.main()