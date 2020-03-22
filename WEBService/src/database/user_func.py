import database


def insert_user(values):
    with database.connect() as conn:
        conn.cursor().execute('''INSERT INTO Users(Fname, Lname, Email, Psw)
                              VALUES(?, ?, ?, ?);''', values)
        conn.cursor().commit()


def exctract_user(email):
    pass
