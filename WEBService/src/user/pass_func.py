import hashlib
import random


def crypt_psw(psw, salt):
    our_plus = str([i for i in psw if psw.index(i) % salt == 0])
    psw = psw + our_plus
    return hashlib.sha256(psw.encode('utf-8')).hexdigest()


def generate_salt(string):
    if len(string) <= 4:
        args = [1, 2, 3]
    elif len(string) <= 10:
        args = [1, 2, 3, 5]
    else:
        args = [1, 2, 3, 5, 7]

    return random.choice(args)
