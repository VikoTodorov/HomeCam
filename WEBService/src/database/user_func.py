import database

conn = database.connect()


def insert_user(values):
    with database.connect() as conn:
        conn.cursor().execute('''INSERT INTO Users(Fname, Lname, Email, Psw)
                              VALUES(?, ?, ?, ?);''', values)


def exctract_user(email):
    pass
