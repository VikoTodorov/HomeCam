import database.connect as database

# CREATE DB IF NOT EXISTS AND ONE TABLE FOR USERS AND ONE TABLE FOR STREAM KEYS


def createDB(test_on=False):
    conn = database.connect_to_DB()
    # ID -> Primary key, Email, Pass, First and Last Name and Salt(needet in
    # crypt algorithm
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Users
                          (Id INTEGER PRIMARY KEY AUTOINCREMENT,
                          Fname VARCHAR(128),
                          Lname VARCHAR(128),
                          Email VARCHAR(255),
                          Psw VARCHAR(64),
                          Salt TINYINT NOT NULL);''')
    # ID and Key > primary
    # key the key is referenced to the user which creates it
    conn.cursor().execute('''CREATE TABLE IF NOT EXISTS StreamKeys
                          (Id INTEGER NOT NULL,
                          Skey VARCHAR(64),
                          PRIMARY KEY (Id, Skey),
                          FOREIGN KEY (Id) REFERENCES Users(Id)
                          ON DELETE CASCADE);''')
    conn.close()
