import unittest

import flask

import main
from user import User, pass_func
from database import connect as database
from database import createdb as DB


class TestLogin(unittest.TestCase):
    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

        DB.createDB()
        conn = database.connect_to_DB()
        try:
            sql = '''INSERT INTO Users(Fname, Lname, Email, Psw, Salt)
      VALUES(?, ?, ?, ?, ?);'''
            psw = pass_func.crypt_psw('test', 2)
            values = ('test', 'test', 'test@test', psw, 2)
            conn.cursor().execute(sql, values)
            conn.commit()
        finally:
            conn.close()

    def test_invalid_Email(self):
        result = self.app.post('/login', data=dict(email='lama@lama', psw=''),
                               follow_redirects=True)
        self.assertIn(b'<p> Invalid email or                                        password </p>',
                      result.data)

    def test_invalid_Password(self):
        result = self.app.post('/login',
                               data=dict(email='test@test', psw='lama'),
                               follow_redirects=True)
        self.assertIn(b'<p> Invalid email or                                        password </p>',
                      result.data)

    def test_successful_Login(self):
        result = self.app.post('/login',
                               data=dict(email='test@test', psw='test'),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<a href="/logout">Log out</a>', result.data)

        with self.app as c:
            result = c.get('/homepage')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(flask.session['email'], 'test@test')

    def tearDown(self):
        conn = database.connect_to_DB()
        try:
            sql = "DELETE FROM Users WHERE Email = 'test@test'"
            conn.cursor().execute(sql)
            conn.commit()
        finally:
            conn.close()


class TestRegister(unittest.TestCase):
    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def insert_test(self):
        DB.createDB()
        conn = database.connect_to_DB()
        try:
            sql = '''INSERT INTO Users(Fname, Lname, Email, Psw, Salt)
      VALUES(?, ?, ?, ?, ?);'''
            psw = pass_func.crypt_psw('test', 2)
            values = ('test', 'test', 'test@test', psw, 2)
            conn.cursor().execute(sql, values)
            conn.commit()
        finally:
            conn.close()

    def test_CorrectRegister(self):
        data_user = User(None, 'test', 'test', 'test@test', 'test', None)

        result = self.app.post('/register',
                               data=dict(fname='test',
                                         lname='test',
                                         email='test@test',
                                         psw='test'),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<a href="/logout">Log out</a>', result.data)

        db_user = User.find_user('test@test')
        self.assertEqual(db_user.getFname(), data_user.getFname())
        self.assertEqual(db_user.getLname(), data_user.getLname())
        self.assertEqual(db_user.getEmail(), data_user.getEmail())

        with self.app as c:
            result = c.get('/homepage')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(flask.session['email'], 'test@test')

    def test_UsedEmail(self):
        self.insert_test()
        result = self.app.post('/register',
                               data=dict(fname='test',
                                         lname='test',
                                         email='test@test',
                                         psw='test'),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>You can&#39;t use                                        that email</p>",
                      result.data)

    def test_FnameRequired(self):
        result = self.app.post('/register',
                               data=dict(fname='',
                                         lname='test',
                                         email='test@test',
                                         psw='test'),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>First name                                  is required</p>",
                      result.data)

    def test_LnameRequired(self):
        result = self.app.post('/register',
                               data=dict(fname='test',
                                         lname='',
                                         email='test@test',
                                         psw='test'),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Last name                                  is required</p>",
                      result.data)

    def test_EmailRequired(self):
        result = self.app.post('/register',
                               data=dict(fname='test',
                                         lname='test',
                                         email='',
                                         psw='test'),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Email                                  is required</p>",
                      result.data)

    def test_PassRequired(self):
        result = self.app.post('/register',
                               data=dict(fname='test',
                                         lname='test',
                                         email='test@test',
                                         psw=''),
                               follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<p>Password                                  is required</p>",
                      result.data)

    def tearDown(self):
        conn = database.connect_to_DB()
        try:
            sql = "DELETE FROM Users WHERE Email = 'test@test'"
            conn.cursor().execute(sql)
            conn.commit()
        finally:
            conn.close()


if __name__ == '__main__':
    unittest.main()
