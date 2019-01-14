# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import sqlite3   # enable control of an sqlite database
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

        c.execute('INSERT INTO avatars VALUES (?,?,?,?)', (username, 'eyes', 'eyes1', '0'))
        c.execute('INSERT INTO avatars VALUES (?,?,?,?)', (username, 'noses', 'nose2', '0'))
        c.execute('INSERT INTO avatars VALUES (?,?,?,?)', (username, 'mouths', 'mouth1', '0'))
        c.execute('INSERT INTO avatars VALUES (?,?,?,?)', (username, 'color', 'FFFF33', '0'))

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

#======PROJECTS FXNS========

def add_project(pid, username, p_name):
    '''
    ADDS A PROJECT TO THE TABLE OF PROJECTS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('INSERT INTO projects VALUES (?,?,?)', (pid, username, p_name))

    db.commit()
    db.close()


def get_project(id):
        '''
        RETURNS p_name GIVEN id
        '''
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        cmd = 'SELECT p_name FROM projects WHERE pid = "{0}"'.format(id)
        c.execute(cmd)
        selectedVal = c.fetchone()

        db.close()

        return selectedVal[0]

def get_projects(username, sort=False):
        '''
        RETURNS A DICTIONARY OF PROJECTS WITH PAIRS OF p_name: pid THAT CORRESPOND TO THE username
        '''
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        command = 'SELECT pid, p_name FROM projects WHERE username = "{0}"'.format(username)
        c.execute(command)

        selectedVal = c.fetchall()
        db.close()

        projects = {}
        for i in selectedVal:
            projects[i[1]] = i[0]
        if sort:
            sorted_projects = {}
            for key in sorted(projects.keys()):
                sorted_projects[key] = projects[key]
            return sorted_projects
        return projects

def remove_project(self, pid):
        '''
        REMOVE A PROJECT FROM THE PROJECT TABLE GIVEN pid
        '''
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()

        cmd = 'DELETE FROM projects WHERE pid = {0}'.format(pid)
        c.execute(cmd)

        db.commit()
        db.close()

        return True


#======PROFILE FXNS========
def get_info(username):
    '''
    RETURNS (first, last, email, phone, bio) OF username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT first_name, last_name, email, phone_num, bio FROM profiles WHERE username = (?)', (username,))
    data = c.fetchone()

    #print(data)
    db.close()

    return data

def get_profile(username):
    '''
    RETURNS A DICTIONARY OF user PROFILE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT first_name, last_name, email, phone_num, bio FROM profiles where username = (?)', (username))

    selectedVal = c.fetchone()
    profile = {}

    profile['first_name'] = selectedVal[0]
    profile['last_name'] = selectedVal[1]
    rofile['email'] = selectedVal[2]
    profile['phone_num'] = selectedVal[3]
    profile['bio'] = selectedVal[4]

    db.close()

    return profile

def set_first_name(username, first_name):
    '''
    SET THE first_name OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET first_name = (?) WHERE username = (?)', (first_name, username))

    db.commit()
    db.close()

    return True

def set_last_name(username, last_name):
    '''
    SET THE last_name OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET last_name = (?) WHERE username = (?)', (last_name, username))

    db.commit()
    db.close()

    return True

def set_email(username, email):
    '''
    SET THE email OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET email = (?) WHERE username = (?)', (email, username))

    db.commit()
    db.close()

    return True

def set_phone(username, phone_num):
    '''
    SET THE phone_num OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET phone_num = (?) WHERE username = (?)', (phone_num, username))

    db.commit()
    db.close()

    return True

def set_bio(username, bio):
    '''
    SET THE bio OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET bio = (?) WHERE username = (?)', (bio, username))

    db.commit()
    db.close()

    return True
#======TASKS FXNS========

def add_task(pid, username, task, description, priority, due_date, status):
    '''
    ADDS A ROW TO tasks TABLE OF INPUT VALUES pid, username, task, description, priority, due_date, and status
    @priority is the only int
    other inputs are strings
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = (pid, username, task, description, priority, due_date, status)

    c.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?)', data)

    db.commit()
    db.close()

    return True

def remove_task(pid, username, task):
    '''
    REMOVES A ROW FROM tasks GIVEN pid, username, and task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM tasks WHERE pid = (?) AND username = (?) AND task = (?)', (pid, username, task))

    db.commit()
    db.close()

    return True

def get_tasks(self, pid, username):
    '''
    RETURNS A DICTIONARY OF tasks FOR THE username IN THE FORMAT task: (description, priority, due_date, status)
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT task, description, priority, due_date, status FROM tasks where pid = (?) AND username = (?)', (pid, username))

    selectedVal = c.fetchall()
    task_dict = {}
    for i in selectedVal:
        task_dict[i[0]] = (i[1], i[2], i[3], i[4])

    db.commit()
    db.close()

    return task_dict

def set_description(description, pid, username, task):
    '''
    SET THE description OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE tasks SET description = (?) WHERE pid = (?) AND username = (?) AND task = (?)', (description, pid, username, task))

    db.commit()
    db.close()

    return True

def set_priority(self, priority, pid, username, task):
    '''
    SET THE priority OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE tasks SET priority = (?) WHERE pid = (?) AND username = (?) AND task = (?)', (priority, pid, username, task))

    db.commit()
    db.close()

    return True

def set_due_date(self, due_date, pid, username, task):
    '''
    SET THE due_date OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE tasks SET due_date = (?) WHERE pid = (?) AND username = (?) AND task = (?)', (due_date, pid, username, task))

    db.commit()
    db.close()

    return True

def set_status(self, status, pid, username, task):
    '''
    SET THE status OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('UPDATE tasks SET status = "{0}" WHERE pid = (?) AND username = (?) AND task = (?)', (status, pid, username, task))

    db.commit()
    db.close()

    return True

#=====MESSAGES FXNS=====
def add_msg(pid, address, user, msg, msg_id, timestamp, private=0):
    '''
    ADDS A ROW TO msgs TABLE OF INPUT VALUES pid, address, user, msg, msg_id, and private
    ALL INPUTS ARE STRINGS EXCEPT private
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = (pid, address, user, msg, msg_id, timestamp)
    if private == 1:
        c.execute('INSERT INTO p_msgs VALUES(?, ?, ?, ?, ?, ?)', data)
        db.commit()
        db.close()
        return True

    c.execute('INSERT INTO t_msgs VALUES(?, ?, ?, ?, ?, ?)', data)
    db.commit()
    db.close()
    return True

def remove_msg(msg_id, private=0):
    '''
    REMOVES A ROW FROM msgs GIVEN pid and msg_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if private == 1:
        c.execute('DELETE FROM p_msgs WHERE  msg_id = (?)', (msg_id))
        db.commit()
        db.close()
        return True
    c.execute('DELETE FROM t_msgs WHERE msg_id = (?)', (msg_id))
    db.commit()
    db.close()
    return True

def get_msgs(pid, private = 0):
    '''
    RETURNS A LIST OF MESSAGE TUPLES GIVEN pid
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if private == 1:
        c.execute('SELECT address, user, msg, msg_id, timestamp FROM p_msgs WHERE pid = (?)', (pid,))
        selectedVal = c.fetchall()
        messages = []
        for i in selectedVal:
            messages.append(i)
        db.commit()
        db.close()
        print(messages)
        return messages

    c.execute('SELECT address, user, msg, msg_id, timestamp FROM t_msgs WHERE pid = (?)', (pid,))
    selectedVal = c.fetchall()
    messages = []
    for i in selectedVal:
        messages.append(i)
    db.commit()
    db.close()
    print(messages)
    return messages

#=====AVATARS FXNS=====

def add_value(value, username, typee):
    '''
    UPDATES VALUES AVAILABLE IN TABLE OF AVATARS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT value FROM avatars WHERE username = (?) AND type = (?)', (username, typee))
    #print('\n\n')
    tuple = c.fetchone()[0].split(',')
    list = []
    for i in tuple:
        if len(i) > 1 and i != None:
            list.append(i)
    if value not in list:
        list.append(value)
    word = ""
    for i in list:
        word += i + ","
    if len(list) > 1:
        #print('length is greater than 1')
        #print(word)
        #print(word[0:len(word) - 1])
        word = word[0:len(word) - 1]
        #print(word)
        
    c.execute('UPDATE avatars SET value = (?) WHERE username = (?) AND type = (?)', (word, username, typee))

    db.commit()
    db.close()

    return True;

def update_current(username, typee, num):
    '''
    UPDATES CURRENT IN TABLE OF AVATARS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('UPDATE avatars SET current = (?) WHERE username = (?) AND type = (?)', (num, username, typee))

    db.commit() #the num is the index of the current
    db.close()

    return True;

def get_value(username, typee):
    '''
    RETURNS TUPLE OF VALUES OF GIVEN TYPE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT value FROM avatars WHERE username = (?) and type = (?)', (username, typee))
    value = c.fetchall()

    db.close()

    return value

def get_current(username, typee):
    '''
    RETURNS CURRENT VALUE OF GIVEN TYPE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT value, current FROM avatars WHERE username = (?) AND type = (?)', (username, typee))

    results = c.fetchall()[0]
    values = results[0]
    currentIndex = results[1]

    current = values.split(',')[int(currentIndex)]
    
    print(current)

    db.close()

    return current

if __name__ == '__main__':
     create_db()

