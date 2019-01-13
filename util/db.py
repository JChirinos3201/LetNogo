# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import sqlite3, uuid   # enable control of an sqlite database
import uuid
from datetime import datetime

DB_FILE = "data/tuesday.db"

def create_db():
    '''
    CREATES TABLE FOR AVATARS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS avatars(username TEXT, type TEXT, value TEXT, current TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS p_msgs(pid TEXT, address TEXT, user TEXT, msg TEXT, msg_id TEXT, timestamp TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS t_msgs(pid TEXT, address TEXT, user TEXT, msg TEXT, msg_id TEXT, timestamp TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT, first_name TEXT, last_name TEXT, email TEXT, phone_num TEXT, bio TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS projects (pid TEXT, username TEXT, p_name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tasks (pid TEXT, username TEXT, task TEXT, description TEXT, priority INT, due_date TEXT, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS notes(username TEXT, note TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS quotes (quote TEXT, author TEXT, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS users (user_name TEXT PRIMARY KEY, passwords TEXT)")

    return True;


def getUsers():
    '''
    RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    cmd = 'SELECT user_name, passwords FROM users'
    c.execute(cmd)
    selectedVal = c.fetchall()

    db.close()
    return dict(selectedVal)

def registerUser(username, password, firstname, lastname, email, phone):
    '''
    REGISTERS USERS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # username is already in database -- do not continue to add

    if findUser(username):
        return False
    # username not in database -- continue to add
    else:
        print('\n\nREGISTERING USER\n\n')
        print('\n\tusername: {}\n\tPassword: {}\n\tFirst: {}\n\tLast: {}\n\tEmail: {}\n\tPhone: {}\n\n\n'.format(username, password, firstname, lastname, email, phone))
        c.execute('INSERT INTO users VALUES (?,?)', (username, password))
        c.execute('INSERT INTO profiles VALUES (?,?,?,?,?,?);', (username, firstname, lastname, email, phone, ""))
        #row = (username, "eyes", "", "")
        #self.insertRow('avatars', row)
        #row = (username, "nose", "", "")
        #self.insertRow('avatars', row)
        #row = (username, "mouth", "", "")
        #self.insertRow('avatars', row)
        #print ('works')

        db.commit()
        db.close()

        return True

def findUser(username):
    '''
    CHECKS IF username IS UNIQUE
    '''
    users = getUsers()
    return username in users

def verifyUser(username, password):
    '''
    CHECKS IF username AND password MATCH THOSE FOUND IN DATABASE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT user_name, passwords FROM users WHERE user_name = (?)', (username,))

    selectedVal = c.fetchone()

    db.close()

    if selectedVal == None:
        return False
    if username == selectedVal[0] and password == selectedVal[1]:
        return True
    return False

#======QUOTE FXNS========

def update_quote(quote, author, date):
    '''
    ADDS A QUOTE TO THE TABLE OF QUOTES
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('DELETE FROM quotes')
    c.execute('INSERT INTO quotes VALUES(?,?,?)', (quote, author, date))

    db.commit()
    db.close()

    return True;

def get_quote():
    '''
    RETURNS A DICTIONARY OF QUOTES
    '''
    dict = {"quote":[], "date": [], "author":[]}

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT quote, author, date FROM quotes')

    data = c.fetchall()
    print(data)

    if len(data)  == 0:
        dict['quote'] = ''
        dict['date'] = ''
        dict['author'] = ''
        #print(dict)

    else:
        dict['quote'] = data[0][0]
        dict['date'] = data[0][2]
        dict['author'] = data[0][1]

    db.close()
    return dict

if __name__ == '__main__':
     create_db()
