import sqlite3
from distutils.util import execute

# Connect to the SQLite database (creates the file if it doesn't exist)
connect = sqlite3.connect('data.db')

# Create a cursor object to execute SQL commands
exe = connect.cursor()

# Execute the CREATE TABLE command
exe.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin BOOLEAN DEFAULT FALSE,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        birthDate DATE NOT NULL,
        password TEXT NOT NULL,
        department TEXT NOT NULL
    )
''')

def addUser(firstName, lastName, birthDate, password, department, admin):
    exe.execute(f'''
        INSERT INTO users (firstName, lastName, birthDate, password, department, admin) VALUES ('{firstName}', '{lastName}', '{birthDate}', '{password}', '{department}','{admin}')    
    ''')

#addUser('User','Name', '04/16/2003', 'TheAdminPass','Student', 'True')

# Commit the changes to the database
connect.commit()

# Close the connection
connect.close()
