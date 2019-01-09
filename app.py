# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages

from util import database

#============instantiate Flask object================
app = Flask(__name__)
app.secret_key = os.urandom(32)

#===========manage user data here====================

DB_FILE = 'data/tuesday.db'
user = None

def setUser(userName):
    '''
    Sets the user global variable to userName
    '''
    global user
    user = userName



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if user == None:
        return redirect(url_for('index'))
    return render_template('landing.html', username = user)

@app.route('/project')
def project():
    return render_template('project.html', username = user)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    '''
    References DB_FILE and handles authentication and registration
    '''
    if user in session:
        return redirect(url_for('index'))
    data = database.DB_Manager(DB_FILE)
    username, password = request.form['username'], request.form['password']

    #=====LOG IN=====
    print(request.form['submit'])
    if request.form['submit'] == 'Login':
        # username and password are valid
        if len(username.strip()) != 0 and len(password.strip()) != 0 and data.verifyUser(username, password):
            session[username] = password
            setUser(username)
            data.save()
            return redirect(url_for('home'))
        # user was found but password is incorrect
        elif data.findUser(username):
            flash('Incorrect password!')
        # user not found in DB at all
        else:
            flash('Incorrect username!')
        data.save()

    #=====REGISTER=====
    else:
        if len(username.strip()) != 0 and not data.findUser(username):
            if len(password.strip()) != 0:
                # add account to DB
                data.registerUser(username, password)
                data.save()
                flash('Successfully registered account for user "{0}"'.format(username))
            else:
                flash('Password length insufficient!')
        elif len(username.strip()) == 0:
            flash('Username length insufficient!')
        else:
            flash('Username already exists!')
    # try again
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    '''
    Logs user out if logged if logged in
    '''
    session.pop(user, None)
    setUser(None)
    flash('Successfully logged out!')
    return redirect(url_for('index'))



@app.route('/get_snippet')
def get_snippet():
    snippet = request.args['snippet']
    if snippet in ['login', 'register']:
        return render_template('{}SNIPPET.html'.format(snippet))
    else:
        return 'Invalid Snippet!'


if __name__ == '__main__':
    app.debug = True
    app.run()
