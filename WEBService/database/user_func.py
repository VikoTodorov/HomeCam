import database.connect as database


def insert_user(values):
    conn = database.connect_to_DB()
    sql = '''INSERT INTO Users(Fname, Lname, Email, Psw, Salt)
    VALUES(?, ?, ?, ?, ?);'''
    conn.cursor().execute(sql, values)
    conn.commit()
    conn.close()


def extract_user(email):
    conn = database.connect_to_DB()
    sql = 'SELECT * FROM Users WHERE Email = ?;'
    result = conn.cursor()
    result.execute(sql, (email, ))
    return result.fetchone()
    # that is an interesting bug
    # conn.cursor().execute(sql, (email, ))
    # return conn.cursor().fetchone()
    conn.close()
