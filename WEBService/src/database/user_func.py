import database
from mysql.connector import Error


def insert_user(values):
    conn = database.connect()
    conn.connect(database='OurDB')
    try:
        conn.cursor().execute('''INSERT INTO Users(Fname, Lname, Email, Psw)
                              VALUES(%s, %s, %s, %s);''', values)
        conn.commit()
    except Error as e:
        print(e)


def extract_user(email):
    conn = database.connect()
    conn.connect(database="OurDB")
    try:
        return conn.cursor().execute('SELECT * FROM Users WHERE Email = ?', \
                                            ((email, ))).fetchone()
    except Error as e:
        print(e)
