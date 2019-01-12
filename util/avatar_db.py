def creates_avatars(self):
    '''
    CREATES TABLE FOR AVATARS
    '''
    def gen_table(tableName, col0, col1, col2, col3,):
        '''
        CREATES A 6 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        if not self.isInDB(tableName):
            command = 'CREATE TABLE "{0}"({1}, {2}, {3}, {4}, {5}, {6})'.format(tableName, col0, col1, col2, col3)
            c.execute(command)
        gen_table('avatars', 'username TEXT', 'type TEXT', 'value TEXT', 'current TEXT')

def add_value(self, value, username, type):
    '''
    UPDATES VALUES AVAILABLE IN TABLE OF AVATARS
    '''
    c = self.openDB()
    command_tuple = (username, type)
    c.execute('SELECT value from avatars WHERE username = ? and type = ?', command_tuple)
    types_string = c.fetchall()[0]
    print(types_string)
    command_tuple = (value, username, type)
    c.execute('UPDATE avatars SET value = ? WHERE username = ? and type = ?', command_tuple)
    return True;

def update_current(self, username, type, num):
    '''
    UPDATES CURRENT IN TABLE OF AVATARS
    '''
    c = self.openDB()
    command_tuple = (num, username, type)
    c.execute('UPDATE avatars SET current = ? WHERE username = ? and type = ?', command_tuple)
    return True;

def getValues(self, username, type):
    '''
    RETURNS DICTIONARY OF VALUES OF GIVEN TYPE
    '''
    c = self.openDB()
    command_tuple = (username, type)
    c.execute('SELECT value FROM avatars WHERE username = ? and type = ?', command_tuple)
    dict = {type: []}
    dict[type] = c.fetchall()
    return dict

def getCurrent (self, username, type):
        '''
        RETURNS CURRENT VALUE OF GIVEN TYPE
        '''
        c = self.openDB()
        command_tuple = (username, type)
        c.execute('SELECT current FROM avatars WHERE username = ? and type = ?', command_tuple)
        return c.fetchone()[0]
