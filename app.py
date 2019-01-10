# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
import datetime
import uuid # tentative

from util import database, api

#============instantiate Flask object================
app = Flask(__name__)
app.secret_key = os.urandom(32)

#===========manage user data here====================

DB_FILE = 'data/tuesday.db'


@app.route('/')
def index():
    data = database.DB_Manager(DB_FILE)

    today = datetime.datetime.today().strftime('%Y-%m-%d')

    api.checkQuote()

    data = database.DB_Manager(DB_FILE)
    quote = data.get_quote()
    data.save()

    return render_template('index.html', quote = quote)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('landing.html', username = session['username'])

@app.route('/profile')
def profile():
    username = session['username']
    
    url = api.getAvatarLink(str(250), username)
    return render_template('profile.html', username = username, url = url)

@app.route('/new_project', methods=["POST"])
def new_project():
    if 'username' not in session:
        return redirect(url_for('index'))

    data = database.DB_Manager(DB_FILE)
    print(request.form)
    projectName = request.form['newProjectName']
    pid = str(uuid.uuid1())

    print('CREATING NEW PROJECT\n\tProject Name: {}\n\tProject ID: {}\n\tUsername: {}\n'.format(projectName, pid, session['username']))
    data.add_project(pid, session['username'], projectName)
    data.save()

    return redirect(url_for('home'))

@app.route('/join_project', methods=["POST"])
def join_project():
    '''
    user joins a project
    '''
    if 'username' not in session:
        return redirect(url_for('index'))
    data = database.DB_Manager(DB_FILE)
    id = str(request.form['id'])
    title = data.get_project(id)
    data.add_project(id, session['username'], title)
    data.save()
    return redirect(url_for('home'))

@app.route('/project/<title>/<id>')
def project(title, id):
    if 'username' not in session:
        return redirect(url_for('index'))
    '''
    pull project info here???
    <fill me XD>
    '''
    return render_template('project.html', username = session['username'], project_name = title)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    '''
    References DB_FILE and handles authentication and registration
    '''
    data = database.DB_Manager(DB_FILE)
    username, password = request.form['username'], request.form['password']

    #=====LOG IN=====
    if 'submit' not in request.form:
        return redirect(url_for('index'))
    print(request.form['submit'])
    if request.form['submit'] == 'Login':
        # username and password are valid
        if len(username.strip()) != 0 and len(password.strip()) != 0 and data.verifyUser(username, password):
            session['username'] = username
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
    if 'username' not in session:
        return redirect(url_for('index'))
    session.pop('username', None)
    flash('Successfully logged out!')
    return redirect(url_for('index'))


@app.route('/get_snippet')
def get_snippet():
    snippet = request.args['snippet']
    if snippet in ['login', 'register', 'projectList', 'newProject', 'joinProject']:
        print('Getting snippet: {}'.format(snippet))
        if snippet == 'projectList' and 'username' in session:
            data = database.DB_Manager(DB_FILE)
            projectDict = data.get_projects(session['username'])
            print('Project dict: {}'.format(projectDict))
            return render_template('{}SNIPPET.html'.format(snippet), projectDict=projectDict)
        return render_template('{}SNIPPET.html'.format(snippet))
    else:
        return 'Invalid Snippet!'

@app.route('/get_avatar')
def get_avatar():
    username = session['username']
    url = api.getAvatarLink(str(50), username)
    print('GETTING AVATAR\n\tUsername: {}\n\tURL: {}\n'.format(username, url))
    return url

if __name__ == '__main__':
    app.debug = True
    app.run()
