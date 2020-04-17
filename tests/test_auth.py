import unittest
from mysql.connector import Error

import flask

# sys.path.append('..')

import main
from user import pass_func
from database import connect


class TestLogin(unittest.TestCase):
    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()
        conn = connect.connect_to_DB()
        conn.connect(database='OurDB')
        try:
            sql = '''INSERT INTO Users(Fname, Lname, Email, Psw, Salt)
          VALUES(%s, %s, %s, %s, %s);'''
            psw = pass_func.crypt_psw('test', 2)
            values = ('test', 'test', 'test@test', psw, 2)
            conn.cursor().execute(sql, values)
            conn.commit()
        except Error as e:
            print(e)

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
        conn = connect.connect_to_DB()
        conn.connect(database='OurDB')
        try:
            sql = "DELETE FROM Users WHERE Email = 'test@test'"
            conn.cursor().execute(sql)
            conn.commit()
        except Error as e:
            print(e)

        finally:
            conn.close()


if __name__ == '__main__':
    unittest.main()
