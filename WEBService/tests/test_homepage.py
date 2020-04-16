import sys
import unittest

import flask

sys.path.append('..')
import main


class TestIndexAndHomepage(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_index_nologged(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b' <a href="/register">Register</a>\n  <a href="/login">Login</a>', result.data)

    def test_index_logged(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['email'] = 'test@test'
        result = self.app.get('/', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<a href="/logout">Log out</a>', result.data)

    def test_homepage_nologged(self):
        result = self.app.get('/homepage', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/login" method="post" class=\'login\'>\n    <p>  </p>\n    <input type="email" name="email" placeholder="Email"/>', result.data)

    def test_homepage_logged(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['email'] = 'test@test'
        result = self.app.get('/homepage')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<a href="/logout">Log out</a>', result.data)


if __name__ == '__main__':
    unittest.main()
