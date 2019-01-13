# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import sqlite3, uuid   # enable control of an sqlite database
import random
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
    c.execute("CREATE TABLE IF NOT EXISTS users (user_name TEXT, passwords TEXT, user_id INTEGER)")

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

def registerUser(userName, password, frist, lsat, email, phone):
    '''
    REGISTERS USERS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    cmd = 'SELECT user_id FROM users WHERE user_id = (SELECT max(user_id) FROM users)'
    c.execute(cmd)
    
    selectedVal = c.fetchone()
    max_id = 0
    if selectedVal != None:
        max_id = selectedVal[0]
    else:
        max_id = 0
        # userName is already in database -- do not continue to add

    if findUser(userName):
        return False
    # userName not in database -- continue to add
    else:
        c.execute('INSERT INTO users VALUES (?,?,?);', (userName, password, max_id + 1))
        c.execute('INSERT INTO profiles VALUES (?,?,?,?);', (frist, lsat, email, phone))
        #row = (userName, "eyes", "", "")
        #self.insertRow('avatars', row)
        #row = (userName, "nose", "", "")
        #self.insertRow('avatars', row)
        #row = (userName, "mouth", "", "")
        #self.insertRow('avatars', row)
        #print ('works')

        db.commit()
        db.close()

        return True

def findUser(userName):
    '''
    CHECKS IF userName IS UNIQUE
    '''
    users = getUsers()
    return userName in users

def verifyUser(userName, password):
    '''
    CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    cmd = ('SELECT user_name, passwords FROM users WHERE user_name = (?)', (userName))
    c.execute(cmd)
    
    selectedVal = c.fetchone()

    db.close()
    
    if selectedVal == None:
        return False
    if userName == selectedVal[0] and password == selectedVal[1]:
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
