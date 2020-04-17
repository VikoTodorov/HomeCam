import database.connect as database

# CREATE DB IF NOT EXISTS AND ONE TABLE FOR USERS AND ONE TABLE FOR STREAM KEYS


def createDB(test_on=False):
    if (test_on == False):
        conn = database.connect_to_DB()

        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS OurDB")
        conn.connect(database="OurDB")
    else:
        conn = database.connect_to_TestDB()
        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS Test")
        conn.connect(database="Test")
    # ID -> Primary key, Email, Pass, First and Last Name and Salt(needet in
    # crypt algorithm
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Users
                          (Id INT AUTO_INCREMENT PRIMARY KEY,
                          Email VARCHAR(255),
                          Fname VARCHAR(128),
                          Lname VARCHAR(128),
                          Psw VARCHAR(64),
                          Salt TINYINT NOT NULL);''')
    # ID and Key > primary
    # key the key is referenced to the user which creates it
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS StreamKeys
                          (Id INT NOT NULL,
                          Skey VARCHAR(64),
                          PRIMARY KEY (Id, Skey),
                          FOREIGN KEY (Id) REFERENCES Users(Id)
                          ON DELETE CASCADE);''')
    conn.close()
