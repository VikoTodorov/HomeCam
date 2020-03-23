from mysql.connector import Error

import database.connect as database


def insert_user(values):
    conn = database.connect_to_DB()
    conn.connect(database='OurDB')
    try:
        sql = '''INSERT INTO Users(Fname, Lname, Email, Psw, Salt)
        VALUES(%s, %s, %s, %s, %s);'''
        conn.cursor().execute(sql, values)
        conn.commit()
    except Error as e:
        print(e)


def extract_user(email):
    conn = database.connect_to_DB()
    conn.connect(database="OurDB")
    try:
        sql = 'SELECT * FROM Users WHERE Email = %s;'
        result = conn.cursor()
        result.execute(sql, (email, ))
        return result.fetchone()
        # that is an interesting bug
        # conn.cursor().execute(sql, (email, ))
        # return conn.cursor().fetchone()
    except Error as e:
        print(e)
