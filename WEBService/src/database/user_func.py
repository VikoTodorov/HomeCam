import database
from mysql.connector import Error


def insert_user(values):
    conn = database.connect()
    conn.connect(database='OurDB')
    try:
        conn.cursor().execute('''INSERT INTO Users(Id, Fname, Lname, Email, Psw)
                              VALUES(NULL, ?, ?, ?, ?);''', values)
        conn.cursor().commit()
    except Error as e:
        print(e)


def extract_user(email):
    pass
