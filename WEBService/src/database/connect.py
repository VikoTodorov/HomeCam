import mysql.connector
from mysql.connector import Error


def connect():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       user='viko',
                                       password='mysqlpsw')
        if conn.is_connected():
            return conn
    except Error as e:
        print(e)
    finally:
        # con.close()
        pass
