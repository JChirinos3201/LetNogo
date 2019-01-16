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

    c.execute("CREATE TABLE IF NOT EXISTS avatars(username TEXT, type TEXT, value TEXT, current INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS p_msgs(pid TEXT, address TEXT, user TEXT, msg TEXT, msg_id TEXT, timestamp TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS t_msgs(pid TEXT, user TEXT, msg TEXT, msg_id TEXT, timestamp TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT, first_name TEXT, last_name TEXT, email TEXT, phone_num TEXT, bio TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS projects (pid TEXT, username TEXT, p_name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS tasks (pid TEXT, username TEXT, task TEXT, description TEXT, priority INTEGER, due_date TEXT, status INTEGER, taskID TEXT, beenCompleted INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS notes(username TEXT, note TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS quotes (quote TEXT, author TEXT, date TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS users (user_name TEXT PRIMARY KEY, passwords TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS currency (user_name TEXT PRIMARY KEY, bigcoin INTEGER)")

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
        c.execute('INSERT INTO currency VALUES (?, ?)', (username, 0))
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

    c.execute('SELECT user_name, passwords FROM users WHERE user_name=?', (username,))

    selectedVal = c.fetchone()

    db.close()

    if selectedVal == None:
        return False
    if username == selectedVal[0] and password == selectedVal[1]:
        return True
    return False

def getUserBigcoin(username):
    '''
    RETURNS AMOUNT OF bigcoin username HAS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT bigcoin FROM currency WHERE user_name=?', (username,))
    selectedVal = c.fetchone()
    db.commit()
    db.close()
    return selectedVal[0]

def setUserBigcoin(username, bigcoin):
    '''
    UPDATES AMOUNT OF bigcoin username HAS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE currency SET bigcoin = ? WHERE user_name = ?', (bigcoin, username, ))
    db.commit()
    db.close()
    return True

def changeUserBigcoin(username, delta):
    '''
    UPDATES AMOUNT OF bigcoin username HAS BY THE DELTA AMOUNT
    RETURNS NEW AMOUNT
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT bigcoin FROM currency WHERE user_name = ?', (username,))
    initial_amt = c.fetchone()[0]
    new_amt = initial_amt + delta
    c.execute('UPDATE currency SET bigcoin = ? WHERE user_name = ?', (new_amt, username))
    db.commit()
    db.close()
    return new_amt

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

    if selectedVal == None:
        return None

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

def verify_project(pid):
    '''
    RETURNS TRUE IF PID IS AN EXISTING PID
    ELSE FALSE 
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    cmd = 'SELECT pid FROM projects'
    c.execute(cmd)

    pids = c.fetchall()

    for each in pids:
        if each[0] == pid:
            return True
    return False

    #print(pids)

def remove_project(pid):
    '''
    REMOVE A PROJECT FROM THE PROJECT TABLE GIVEN pid
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    cmd = 'DELETE FROM projects WHERE pid = "{0}"'.format(pid)
    c.execute(cmd)

    db.commit()
    db.close()

    return True

def get_teammates(pid):
    '''
    RETURNS TUPLE OF TEAMMATES
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT username FROM projects WHERE pid=?', (pid,))
    data = c.fetchall()

    db.commit()
    db.close()

    return data

#======PROFILE FXNS========
def get_info(username):
    '''
    RETURNS (first, last, email, phone, bio) OF username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT first_name, last_name, email, phone_num, bio FROM profiles WHERE username=?', (username,))
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

    c.execute('SELECT first_name, last_name, email, phone_num, bio FROM profiles where username=?', (username))

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
    c.execute('UPDATE profiles SET first_name = ? WHERE username =?', (first_name, username))

    db.commit()
    db.close()

    return True

def set_last_name(username, last_name):
    '''
    SET THE last_name OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET last_name = ? WHERE username =?', (last_name, username))

    db.commit()
    db.close()

    return True

def set_email(username, email):
    '''
    SET THE email OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET email = ? WHERE username=?', (email, username))

    db.commit()
    db.close()

    return True

def set_phone(username, phone_num):
    '''
    SET THE phone_num OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET phone_num=? WHERE username=?', (phone_num, username))

    db.commit()
    db.close()

    return True

def set_bio(username, bio):
    '''
    SET THE bio OF A ROW IN tasks GIVEN username
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE profiles SET bio = ? WHERE username=?', (bio, username))

    db.commit()
    db.close()

    return True

#======TASKS FXNS========

def add_task(pid, username, task, description, priority, due_date, status):
    '''
    ADDS A ROW TO tasks TABLE OF INPUT VALUES pid, username, task, description, priority, due_date, status, and taskID
    @priority is the only int
    other inputs are strings
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    taskID = str(uuid.uuid1())
    data = (pid, username, task, description, priority, due_date, status, taskID, 0)

    c.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', data)

    db.commit()
    db.close()

    return True

def remove_task(taskID):
    '''
    REMOVES A ROW FROM tasks GIVEN pid, username, and task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM tasks WHERE taskID=?', (taskID))

    db.commit()
    db.close()

    return True

def get_tasks_pid(pid):
    '''
    RETURNS A LIST OF TUPLES FOR THE pid IN THE FORMAT [(task, description, priority, due_date, status, taskID)...]
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT task, description, priority, due_date, status, taskID FROM tasks WHERE pid=?', (pid,))
    selectedVals = c.fetchall()
    tasks = []
    for i in selectedVals:
        tasks.append(i)
    db.commit()
    db.close()
    return tasks


def get_tasks_username(pid, username):
    '''
    RETURNS A DICTIONARY OF tasks FOR THE username IN THE FORMAT {task: (description, priority, due_date, status, taskID)}
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT task, description, priority, due_date, status, taskID FROM tasks where pid=? AND username=?', (pid, username))

    selectedVals = c.fetchall()
    tasks = []
    for i in selectedVals:
        tasks.append(i)
    db.commit()
    db.close()
    return tasks

def set_description(description, taskID):
    '''
    SET THE description OF A ROW IN tasks GIVEN taskID
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE tasks SET description = ? WHERE taskID=?', (taskID))

    db.commit()
    db.close()

    return True

def set_priority(priority, taskID):
    '''
    SET THE priority OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE tasks SET priority = ? WHERE taskID=?', (priority, taskID))

    db.commit()
    db.close()

    return True

def set_due_date(due_date, taskID):
    '''
    SET THE due_date OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('UPDATE tasks SET due_date = ? WHERE taskID=?', (due_date, taskID))

    db.commit()
    db.close()

    return True

def set_status(status, taskID):
    '''
    SET THE status OF A ROW IN tasks GIVEN pid, username, AND task
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    print('damn son')

    c.execute('SELECT beenCompleted FROM tasks WHERE taskID=(?)', (taskID,))
    #print(taskID)
    been = c.fetchone()[0]
    print(been)
    
    
    if status == 2 and been == 0:
        print('status is 2')
        c.execute('UPDATE tasks SET beenCompleted = 1 WHERE taskID=?', (taskID,)) #setUserBigcoin getUserBigcoin changeUserBigcoin
        c.execute('SELECT priority, username FROM tasks WHERE taskID=?', (taskID,))
        
        data = c.fetchall()[0]
        p = data[0]
        username = data[1]

        db.commit()
        db.close()
        
        changeUserBigcoin(username, 50 + 50 * p)

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    
    c.execute('UPDATE tasks SET status = ? WHERE taskID=?', (status, taskID))

    db.commit()
    db.close()

    return True

#=====MESSAGES FXNS=====
def add_t_msg(pid, user, msg, msg_id, timestamp):
    '''
    ADDS A ROW TO msgs TABLE OF INPUT VALUES pid, user, msg, msg_id, and private
    ALL INPUTS ARE STRINGS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = (pid, user, msg, msg_id, timestamp)

    c.execute('INSERT INTO t_msgs VALUES(?, ?, ?, ?, ?)', data)
    db.commit()
    db.close()
    return True

def add_p_msg(pid, address, user, msg, msg_id, timestamp):
    '''
    ADDS A ROW TO msgs TABLE OF INPUT VALUES pid, address, user, msg, msg_id, and private
    ALL INPUTS ARE STRINGS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = (pid, address, user, msg, msg_id, timestamp)
    print("\n\n\nSENDING PM\n\n\tpid: {}\n\tto: {}\n\tfrom: {}\n\tmsg: {}\n\tmsg ID: {}\n\ttimestamp: {}\n\n\n\n".format(pid, address, user, msg, msg_id, timestamp))

    c.execute('INSERT INTO p_msgs VALUES(?, ?, ?, ?, ?, ?)', data)

    db.commit()
    db.close()
    return True

def remove_t_msg(msg_id):
    '''
    REMOVES A ROW FROM msgs GIVEN pid and msg_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('DELETE FROM t_msgs WHERE msg_id=?', (msg_id))
    db.commit()
    db.close()
    return True

def remove_p_msg(msg_id):
    '''
    REMOVES A ROW FROM msgs GIVEN pid and msg_id
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('DELETE FROM p_msgs WHERE  msg_id=?', (msg_id))
    db.commit()
    db.close()
    return True

def get_t_msgs(pid):
    '''
    RETURNS A LIST OF MESSAGE TUPLES GIVEN pid
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT user, msg, msg_id, timestamp FROM t_msgs WHERE pid=?', (pid,))
    selectedVal = c.fetchall()
    messages = []
    for i in selectedVal:
        messages.append(i)
    db.commit()
    db.close()
    print(messages)
    return messages

def get_p_msgs(pid):
    '''
    RETURNS A LIST OF MESSAGE TUPLES GIVEN pid
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT address, user, msg, msg_id, timestamp FROM p_msgs WHERE pid=?', (pid,))
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

    c.execute('SELECT value FROM avatars WHERE username=? AND type=?', (username, typee))
    #print('\n\n')
    t = c.fetchall()
    t = t[0][0]
    t = t.split(',')
    list = []
    for i in t:
        if len(i) > 1 and i != None:
            list.append(i)
    if value not in list:
        list.append(value)
    word = ','.join(list)

    c.execute('UPDATE avatars SET value = ? WHERE username=? AND type=?', (word, username, typee))

    db.commit()
    db.close()

    return True;

def update_current(username, typee, new):
    '''
    UPDATES CURRENT IN TABLE OF AVATARS
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    vals = get_value(username, typee).split(',')
    if new in vals:

        index = vals.index(new)

        c.execute('UPDATE avatars SET current = ? WHERE username=? AND type=?', (index, username, typee))

        db.commit()
        db.close()

        return True
    db.close()
    return False

def get_value(username, type):
    '''
    RETURNS VALUES OF GIVEN TYPE AS A STRING
    EX. "eyes1,eyes4"
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT value FROM avatars WHERE username=? and type=?', (username, type))
    value = c.fetchall()[0][0]

    db.close()

    return value

def get_current(username, type):
    '''
    RETURNS CURRENT VALUE OF GIVEN TYPE
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT value, current FROM avatars WHERE username=? AND type=?', (username, type))

    tuple = c.fetchall()[0]

    val = tuple[0]
    index = tuple[1]

    current = val.split(',')[index]

    db.close()
    return current

if __name__ == '__main__':
     create_db()
