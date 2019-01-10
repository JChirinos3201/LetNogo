# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import sqlite3   # enable control of an sqlite database
import random
from datetime import datetime

class DB_Manager:
    '''
    HOW TO USE:
    Every method openDB by connecting to the inputted path of
    a database file. After performing all operations on the
    database, the instance of the DB_Manager must save using
    the save method.
    The operations/methods can be found below. DB_Manager
    has been custom fit to work with
    P02: The End
    '''
    def __init__(self, dbfile):
        '''
        SET UP TO READ/WRITE TO DB FILES
        '''
        self.DB_FILE = dbfile
        self.db = None
    #========================HELPER FXNS=======================
    def openDB(self):
        '''
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        '''
        self.db = sqlite3.connect(self.DB_FILE) # open if file exists, otherwise create
        return self.db.cursor()

    def tableCreator(self, tableName, col0, col1, col2):
        '''
        CREATES A 3 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        c = self.openDB()
        if not self.isInDB(tableName):
            command = 'CREATE TABLE "{0}"({1}, {2}, {3});'.format(tableName, col0, col1, col2)
            c.execute(command)


    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
       '''
       c = self.openDB()
       command = 'INSERT INTO "{0}" VALUES(?, ?, ?)'
       c.execute(command.format(tableName), data)


    def isInDB(self, tableName):
        '''
        RETURNS True IF THE tableName IS IN THE DATABASE
        RETURNS False OTHERWISE
        '''
        c = self.openDB()
        command = 'SELECT * FROM sqlite_master WHERE type = "table"'
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all tableNames and store in a set
        tableNames = set([x[1] for x in selectedVal])

        return tableName in tableNames

    def table(self, tableName):
        '''
        PRINTS OUT ALL ROWS OF INPUT tableName
        '''
        c = self.openDB()
        command = 'SELECT * FROM "{0}"'.format(tableName)
        c.execute(command)
        #print(c.fetchall())

    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        self.db.commit()
        self.db.close()
    #========================HELPER FXNS=======================

    #======================== DB FXNS =========================
    def createUsers(self):
        '''
        #CREATES TABLE OF users
        '''
        self.tableCreator('users', 'user_name text', 'passwords text', 'user_id integer')
        return True

    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS
        '''
        c = self.openDB()
        command = 'SELECT user_name, passwords FROM users'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def registerUser(self, userName, password):
        '''
        ADDS user TO DATABASE
        '''
        c = self.openDB()
        command = 'SELECT user_id FROM users WHERE user_id = (SELECT max(user_id) FROM users)'
        c.execute(command)
        selectedVal = c.fetchone()
        max_id = 0
        if selectedVal != None:
            max_id = selectedVal[0]
        else:
            max_id = 0
            # userName is already in database -- do not continue to add
        if self.findUser(userName):
            return False
        # userName not in database -- continue to add
        else:
            row = (userName, password, max_id + 1)
            self.insertRow('users', row)
            return True

    def findUser(self, userName):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return userName in self.getUsers()

    def verifyUser(self, userName, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        command = 'SELECT user_name, passwords FROM users WHERE user_name = "{0}"'.format(userName)
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if userName == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    #====================== TUESDAY FXNS ======================

    #======QUOTE FXNS========
    def creates_quotes(self):
        '''
        CREATES TABLE FOR QUOTES
        '''
        self.tableCreator('quotes', 'quote text', 'author text', 'date text')

    def update_quote(self, quote, author, date):
        '''
        ADDS A QUOTE TO THE TABLE OF QUOTES
        '''
        c = self.openDB()
        command_tuple = (quote, author, date)
        c.execute('DELETE FROM quotes')
        c.execute('INSERT INTO quotes VALUES(?,?,?)', command_tuple)
        return True;

    def get_quote(self, date):
        '''
        RETURNS A DICTIONARY OF QUOTES
        '''
        dict = {"quote":[], "date": []}
        c = self.openDB()
        c.execute('SELECT quote FROM quotes WHERE date = "{0}"'.format(date))
        dict['quote'] = c.fetchone()[0]
        c.execute('SELECT date FROM quotes')
        dict['date'] = c.fetchone()[0]
        return today


    #======NOTES FXNS========
    def create_notes(self):
        '''
        CREATES TABLE FOR NOTES
        '''
        c = self.openDB()
        if not self.isInDB('notes'):
            command = 'CREATE TABLE "{0}"({1}, {2});'.format('notes', 'username text', 'note text')
            c.execute(command)

    def add_note(self, username, note):
        '''
        ADDS note FOR username IN NOTES TABLE
        '''
        c = self.openDB()
        def insertNote(data):
           '''
             APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
             @tableName is the name the table being written to
             @data is a tuple containing data to be entered
           '''
           command = 'INSERT INTO "{0}" VALUES(?, ?)'
           c.execute(command.format('notes'), data)
        insertNote((username, note))
        return True

    def remove_note(self, username, note):
        '''
        REMOVES note FOR username IN NOTES TABLE
        '''
        c = self.openDB()
        command = 'DELETE FROM notes WHERE username = "{0}" AND note = "{1}"'.format(username, note)
        c.execute(command)
        return True

    def get_notes(self, username):
        '''
        RETURNS A LIST OF NOTES FOR username
        '''
        c = self.openDB()
        command = 'SELECT note FROM notes WHERE username = "{0}"'
        c.execute(command)
        selectedVal = c.fetchall()
        user_notes = []
        print(selectedVal)
        for i in selectedVal:
            user_notes.append(i[0])
        return user_notes

    #======PROJECTS FXNS========
    def create_projects(self):
        '''
        CREATES TABLE FOR PROJECTS
        '''
        self.tableCreator('projects', 'pid text', 'username text', 'p_name text')

    def add_project(self, pid, username, p_name):
        '''
        ADDS A PROJECT TO THE TABLE OF PROJECTS
        '''
        self.insertRow('projects', (pid, username, p_name))

    def get_projects(self, username, sort=False):
        '''
        RETURNS A DICTIONARY OF PROJECTS WITH PAIRS OF p_name: pid THAT CORRESPOND TO THE username
        '''
        c = self.openDB()
        command = 'SELECT pid, p_name FROM projects WHERE username = "{0}"'.format(username)
        c.execute(command)
        selectedVal = c.fetchall()
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
        c = self.openDB()
        command = 'DELETE FROM projects WHERE pid = {0}'.format(pid)
        c.execute(command)
        return True

    #====================== END OF TUESDAY FXNS ======================


    #======================== DB FXNS =========================
#======================== END OF CLASS DB_Manager =========================

# initiation process and TESTING
'''
DB_FILE = '../data/tuesday.db'
initiate = DB_Manager(DB_FILE)

# TEST QUOTES
#initiate.creates_quotes()
#initiate.update_quote("happy is me", "happy is you", datetime.date(datetime.today()))
#print(initiate.get_quote(datetime.date(datetime.today())))

# TEST USERS
#initiate.createUsers()
#initiate.registerUser('a', 'a')

# TEST NOTES
#initiate.create_notes()

#initiate.add_note('null', 'bang')
#initiate.add_note('null', 'pow')
#initiate.add_note('peej', 'woo')
#print(initiate.get_notes('peej'))

# TEST PROJECTS
#initiate.create_projects()
#initiate.add_project('73', 'null', 'apple')
print(initiate.get_projects('73'))
#initiate.remove_project('73')

#print(initiate.get_projects('null', True))
initiate.save()
'''
