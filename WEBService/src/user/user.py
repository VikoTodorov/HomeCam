import database
import user


class User:
    # first name, last name, email and password
    def __init__(self, fname, lname, email, psw):
        self._fname = fname
        self._lname = lname
        self._email = email
        self._psw = psw

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
        Pass = user.crypt_psw(self._psw)
        values = (self._fname, self._lname, self._email, Pass)
        database.insert_user(values)

    def verify_pass(self, password):
        return self.getPass == user.crypt_psw(password)

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
