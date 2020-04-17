import unittest
import hashlib
import sys

#sys.path.append("...")
from WEBService.user import pass_func

class TestHash(unittest.TestCase):

    def test_hash_with_two(self):
        data = "lala"
        psw = pass_func.crypt_psw(data, 2)
        correct_psw = hashlib.sha256("lalall".encode('utf-8')).hexdigest()
        self.assertEqual(psw, correct_psw)

    def test_hash_with_three(self):
        data = "abracadabra"
        psw = pass_func.crypt_psw(data, 3)
        correct_psw = hashlib.sha256("abracadabraaaadaa".encode('utf-8')).hexdigest()
        self.assertEqual(psw, correct_psw)

    def test_hash_with_five(self):
        data = "abracadabratujemojtalama"
        psw = pass_func.crypt_psw(data, 5)
        correct_psw = hashlib.sha256("abracadabratujemojtalamaaaaaamalama".encode('utf-8')).hexdigest()
        self.assertEqual(psw, correct_psw)


if __name__ == '__main__':
    unittest.main()
