# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
import datetime, uuid, re

from util import db, api

#============instantiate Flask object================
app = Flask(__name__)
app.secret_key = os.urandom(32)

#===========manage user data here====================

DB_FILE = 'data/tuesday.db'
db.create_db()

@app.route('/')
def index():
    
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    api.checkQuote()

    quote = db.get_quote()

    return render_template('index.html', quote = quote)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('landing.html', username = session['username'])

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']

    url = api.getAvatarLink(str(250), username)
    bodyParts = api.bodyParts()
    link = api.customAvatarLink('eyes1', 'nose1', 'mouth1', 'DD00DD')

    return render_template('profile.html', username = username, url = url, link = link)

@app.route('/avatar')
def avatar():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']

    # this will be replaced with data from the db
    eyes_testing = ['eyes1', 'eyes2', 'eyes3', 'eyes4']
    noses_testing = ['noses1', 'noses2', 'noses3', 'noses4']
    mouths_testing = ['mouths1', 'mouths2', 'mouths3', 'mouths4']
    color_testing = ['color1', 'color2', 'color3', 'color4']

    url = api.getAvatarLink(str(285), username)
    return render_template('avatar.html', username = username, url = url, eyes = eyes_testing, noses = noses_testing, mouths = mouths_testing, color = color_testing)

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
    #data = database.DB_Manager(DB_FILE)
    username, password = request.form['username'], request.form['password']
    #=====LOG IN=====
    if 'submit' not in request.form:
        return redirect(url_for('index'))
    print(request.form['submit'])
    if request.form['submit'] == 'Login':
        # username and password are valid
        if len(username.strip()) != 0 and len(password.strip()) != 0 and db.verifyUser(username, password):
            session['username'] = username
            #data.save()
            return redirect(url_for('home'))
        # user was found but password is incorrect
        elif db.findUser(username):
            flash('Incorrect credentials!')
        # user not found in DB at all
        else:
            flash('Incorrect credentials!')
        #data.save()

    #=====REGISTER=====
    else:
        firstname, lastname, email, phone = request.form['firstname'], request.form['lastname'], request.form['email'], request.form['phone']
        if ' ' in username or len(username.strip() == 0):
            flash('Invalid username!')
        elif data.findUser(username):
            flash('Username exists!')
        elif ' ' in password or len(password.strip() == 0):
            flash('Invalid password!')
        elif ' ' in firstname or len(firstname.strip()) == 0:
            flash('Invalid first name!')
        elif ' ' in lastname or len(lastname.strip()) == 0:
            flash('Invalid last name!')
        elif ' ' in email or len(email.strip()) == 0 or '@' not in email or '.' not in email:
            flash('Invalid email address!')
        elif 0 < len(phone.strip()) < 10 or len(phone.strip()) > 10 or re.match('\(\d{3,3}\) \d{3,3}-\d{4,4}', phone) == None:
            flash('Invalid phone number!')
        else:
            data.registerUser(username, password, firstname, lastname, email, phone)
            data.save()
            flash('Successfully registered account for user "{0}"'.format(username))
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
    print('Getting snippet: {}'.format(snippet))
    if snippet == 'projectList' and 'username' in session:
        data = database.DB_Manager(DB_FILE)
        projectDict = data.get_projects(session['username'])
        print('Project dict: {}'.format(projectDict))
        return render_template('{}SNIPPET.html'.format(snippet), projectDict=projectDict)
    return render_template('{}SNIPPET.html'.format(snippet))

@app.route('/get_avatar')
def get_avatar():
    username = session['username']
    url = api.getAvatarLink(str(50), username)
    print('GETTING AVATAR\n\tUsername: {}\n\tURL: {}\n'.format(username, url))
    return url

if __name__ == '__main__':
    app.debug = True
    app.run()
