import mysql.connector
from mysql.connector import Error

# replace the strings in user and password with your personal mysql server datas
def connect():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       user='root',
                                       password='pass')
        if conn.is_connected():
            return conn
    except Error as e:
        print(e)
    finally:
        # con.close()
        pass
