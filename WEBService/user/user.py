from database import user_func as database
from user import pass_func


class User:
    # first name, last name, email and password and secret key
    # all are protected variables
    def __init__(self, Id, fname, lname, email, psw, salt=None):
        self._Id = Id
        self._fname = fname
        self._lname = lname
        self._email = email
        self._psw = psw
        self._salt = salt

    def getFname(self):
        return self._fname

    def getLname(self):
        return self._lname

    def getNames(self):
        return self._fname, self._lname

    def getEmail(self):
        return self._email

    def getPass(self):
        return self._psw

    def create(self):
        salt = pass_func.generate_salt(self._psw)
        Pass = pass_func.crypt_psw(self._psw, salt)
        values = (self._fname, self._lname, self._email, Pass, salt)
        database.insert_user(values)

    def verify_pass(self, password):
        return self.getPass() == pass_func.crypt_psw(password, self._salt)

    @staticmethod
    def find_user(email):
        if not email:
            return None
        else:
            row = database.extract_user(email)
            if row:
                return User(*row)
            else:
                return False
