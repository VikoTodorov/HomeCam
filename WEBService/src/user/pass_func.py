import hashlib
def crypt_psw(psw):
    our_plus = str([i for i in psw if psw.index(i) % 3 == 0])
    psw = psw + our_plus
    return hashlib.sha256(psw.encode('utf-8')).hexdigest()

