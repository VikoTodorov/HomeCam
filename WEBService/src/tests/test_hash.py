import unittest
import hashlib

from user import pass_func


class TestHash(unittest.TestCase):

    def test_normal_hash(self):
        data = "lala"
        psw = pass_func.crypt_psw(data, 2)
        correct_psw = hashlib.sha256("lalall".encode('utf-8')).hexdigest()
        self.assertEqual(psw, correct_psw)


if __name__ == '__main__':
    unittest.main()
