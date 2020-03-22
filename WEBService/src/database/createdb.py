import database 

conn = database.connect()

conn.cursor().execute("CREATE DATABASE IF NOT EXISTS OurDB")
conn.connect(database="OurDB")

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Users
                      (Id INT AUTO_INCREMENT PRIMARY KEY,
                      Email VARCHAR(255),
                      Fname VARCHAR(128),
                      Lname VARCHAR(128),
                      Psw VARCHAR(255));''')

conn.cursor().execute('''CREATE TABLE IF NOT EXISTS Keys
                      (Id INT NOT NULL,
                      Key VARCHAR(255),
                      PRIMARY KEY (Id, Key),
                      FOREIGN KEY (Id) REFERENCES Users(Id)
                      ON DELETE CASCADE);''')
