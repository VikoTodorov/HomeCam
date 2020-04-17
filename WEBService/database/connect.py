import sqlite3


# replace the strings in user and password with your personal mysql
# server datas
def connect_to_DB():
    conn = sqlite3.connect('Test.db')
    return conn
