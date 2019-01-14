# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
import datetime, uuid, re, json

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

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)

    bodyParts = api.bodyParts()
    link = api.customAvatarLink(eyes, nose, mouth, color)

    return render_template('profile.html', username = username, url = url, link = link)

@app.route('/avatar')
def avatar():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']

    # this will be replaced with data from the db
    eyes_testing = ['eyes1', 'eyes2', 'eyes3', 'eyes4']
    noses_testing = ['nose2', 'nose3', 'nose4', 'nose5']
    mouths_testing = ['mouth1', 'mouth3', 'mouth5', 'mouth6']
    color_testing = ['FFFF33', 'C55EB1', '5A6358', '000000']

    url = api.getAvatarLink(str(285), username)
    return render_template('avatar.html', username = username, url = url, eyes = eyes_testing, noses = noses_testing, mouths = mouths_testing, colors = color_testing)

@app.route('/new_project', methods=["POST"])
def new_project():
    if 'username' not in session:
        return redirect(url_for('index'))

    #data = database.DB_Manager(DB_FILE)
    print(request.form)
    projectName = request.form['newProjectName']
    if ' ' in projectName or projectName.strip() == '' or '?' in projectName or '#' in projectName:
        flash('Invalid project name!')
        return redirect(url_for('home'))
    pid = str(uuid.uuid1())

    print('CREATING NEW PROJECT\n\tProject Name: {}\n\tProject ID: {}\n\tUsername: {}\n'.format(projectName, pid, session['username']))
    db.add_project(pid, session['username'], projectName)
    #data.save()

    return redirect(url_for('home'))

@app.route('/new_task', methods=['GET'])
def new_task():
    if 'username' not in session:
        return redirect(url_for('index'))
    print(request.args)
    # pid TEXT, username TEXT, task TEXT, description TEXT, priority INT, due_date TEXT, status TEXT)

    task = request.args['task']
    description = request.args['description']
    priority = request.args['priority']
    due_date = request.args['due_date']
    status = request.args['status']
    pid = request.args['pid']
    db.add_task(pid, session['username'], task, description, priority, due_date, status)

    return 'added {}'.format(task)


@app.route('/join_project', methods=["POST"])
def join_project():
    '''
    user joins a project
    '''
    if 'username' not in session:
        return redirect(url_for('index'))
    id = str(request.form['id'])
    title = db.get_project(id)
    db.add_project(id, session['username'], title)
    return redirect(url_for('home'))

@app.route('/project/<title>/<id>')
def project(title, id):
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('project.html', username = session['username'], project_name = title, p_id = id)

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
        passwordCheck = request.form['passwordConfirmation']
        firstname, lastname, email, phone = request.form['firstname'], request.form['lastname'], request.form['email'], request.form['phone']

        print('\n\nREGISTERING USER\n\n')
        print('\n\tUsername: {}\n\tPassword: {}\n\tPassword Check: {}\n\tFirst: {}\n\tLast: {}\n\tEmail: {}\n\tPhone: {}\n\n\n'.format(username, password, passwordCheck, firstname, lastname, email, phone))

        if password != passwordCheck:
            flash('Passwords don\'t match!')
        elif ' ' in username or len(username.strip()) == 0:
            flash('Invalid username!')
        elif db.findUser(username):
            flash('Username exists!')
        elif ' ' in password or len(password.strip()) == 0:
            flash('Invalid password!')
        elif ' ' in firstname or len(firstname.strip()) == 0:
            flash('Invalid first name!')
        elif ' ' in lastname or len(lastname.strip()) == 0:
            flash('Invalid last name!')
        elif ' ' in email or len(email.strip()) == 0 or '@' not in email or '.' not in email:
            flash('Invalid email address!')
        elif len(phone.strip()) > 0 and re.match('\(?\d{3,3}\)? ?\d{3,3}-?\d{4,4}', phone) == None:
            flash('Invalid phone number! Try the format (XXX) XXX-XXXX')
        else:
            if phone.strip() != "":
                phone = re.match('\(?\d{3,3}\)? ?\d{3,3}-?\d{4,4}', phone).group()
            db.registerUser(username, password, firstname, lastname, email, phone)
            #db.save()
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
        projectDict = db.get_projects(session['username'])
        print('Project dict: {}'.format(projectDict))
        return render_template('{}SNIPPET.html'.format(snippet), projectDict=projectDict)
    if snippet == 'privateInbox' and 'username' in session:
        pid = request.args['pid']
        private_messages = db.get_msgs(pid, 1)
        print(private_messages)
        if (private_messages == []):
            return """<div class="alert alert-warning">You don't have any private messages ;&#40;</div>"""
        return render_template('{}SNIPPET.html'.format(snippet), private_messages = private_messages)
    if snippet == 'tasks' and 'username' in session:
        pid = request.args['pid']
        tasks = db.get_tasks_username(pid, session['username'])
        unstarted = {}
        workingon = {}
        done = {}
        for key in tasks:
            if tasks[key][3] == 0:
                unstarted[key] = tasks[key]
            elif tasks[key][3] == 1:
                workingon[key] = tasks[key]
            else:
                done[key] = tasks[key]
        print('UNSTARTED:\n',unstarted)
        print('WORKINGON:\n',workingon)
        print('DONE:\n',done)
        task_dict = {'unstarted': unstarted, 'workingon': workingon, 'done': done}
        print('TASK_DICT', task_dict)
        return render_template('{}SNIPPET.html'.format(snippet), task_dict = task_dict)
    return render_template('{}SNIPPET.html'.format(snippet))

@app.route('/get_avatar')
def get_avatar():
    username = session['username']

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)
    print('GETTING AVATAR\n\tUsername: {}\n\tURL: {}\n'.format(username, url))
    print(url)
    return url

@app.route('/get_avatar_json')
def get_avatar_json():
    username = session['username']

    d = {}
    d['eyes'] = db.get_current(username, 'eyes')
    d['nose'] = db.get_current(username, 'noses')
    d['mouth'] = db.get_current(username, 'mouths')
    d['color'] = db.get_current(username, 'color')

    return json.dumps(d)

@app.route('/get_info')
def get_info():
    val = request.args['val']
    user = request.args['username']

    userInfo = db.get_info(user)
    pairs = ['first', 'last', 'email', 'phone', 'bio']
    return userInfo[pairs.index(val)]

@app.route('/get_username')
def get_username():
    if 'username' in session:
        return session['username']
    else:
        return 'NOT LOGGED IN'

@app.route('/get_profile_button')
def get_profile_button():
    user = request.args['username']
    req = request.args['val']
    input = ''
    if req == 'Bio':
        input = '<textarea class="form-control" rows="15" maxlength="1000" id="newBio">{}</textarea>'
    else:
        input = '<input type="text" class="form-control" value="{}" id="{}">'

    buttons = '<div class="btn-group" style="display: flex"> <button type="button" class="btn btn-sm btn-danger" style="flex: 1;" onclick="display{}();">Cancel</button> <button type="button" class="btn btn-sm btn-success" style="flex: 1;" onclick="update{}();">Update</button> </div>'

    userInfo = db.get_info(user)
    pairs = ['FirstName', 'LastName', 'Email', 'Phone', 'Bio']

    oldVal = userInfo[pairs.index(req)]

    if req == 'Bio':
        input = input.format(oldVal)
    else:
        input = input.format(oldVal, req)
    buttons = buttons.format(req, req)

    d = {'input': input, 'buttons': buttons}

    return json.dumps(d)

@app.route('/update_info')
def update_info():
    username = request.args['username']
    what = request.args['what']
    newVal = request.args['newVal']

    if what == 'first':
        db.set_first_name(username, newVal)
    elif what == 'last':
        db.set_last_name(username, newVal)
    elif what == 'email':
        db.set_email(username, newVal)
    elif what == 'phone':
        db.set_phone(username, newVal)
    elif what == 'bio':
        db.set_bio(username, newVal)

    return "K we good"

@app.route('/update_avatar')
def update_avatar():
    what = request.args['what']
    newVal = request.args['newVal']
    username = session['username']

    vals = db.get_value(username, what)
    if newVal not in vals:
        db.add_value(newVal, username, what)
    db.update_current(username, what, newVal)

    return "all good, buddy!"

@app.route('/get_avatar_form_get_edition')
def get_avatar_from_get():
    username = request.args['username']

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)
    print('GETTING AVATAR\n\tUsername: {}\n\tURL: {}\n'.format(username, url))
    print(url)
    return url

@app.route('/delete_private_message')
def delete_private_message():
    msgID = request.args['msgID']
    db.remove_msg(msgID, private=1)
    return "All done here, folks!"

@app.route('/get_dashboard')
def get_dashboard():
    username = session['username']
    pid = request.args['pid']
    print("\n\n\nPID: {}\n\n\n".format(pid))

    messages = db.get_msgs(pid)
    print("\n\n\nPRIVATE MESSAGES:\n{}\n\n".format(messages))

    tasks = db.get_tasks_pid(pid)

    print('\n\n\nTASKS\n')
    for i in tasks:
        print('\t{}\n'.format(i))
    print('\n\n')

    if len(tasks) > 0:
        # for status bar
        # [notstarted, working, done]
        statusList = [0, 0, 0]
        for task in tasks:
            statusList[task[4]] += 1
        notstarted = (statusList[0] * 100) // len(tasks)
        working = (statusList[1] * 100) // len(tasks)
        done = 100 - (notstarted + working)

        # for team members tab thing

    else:
        done = notstarted = working = 'no tasks'

    return render_template('dashboardSNIPPET.html', messages=messages[:5], done=str(done), working=str(working), notstarted=str(notstarted), tasks=[])













if __name__ == '__main__':
    app.debug = True
    app.run()
