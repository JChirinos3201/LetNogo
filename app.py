# LetNogo - Joan Chirinos, Susan Lin, Johnny Wong, Thomas Zhao
# SoftDev1 pd8
# P02: The End

import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
import datetime, uuid, re, json, random

from util import db, api

#============instantiate Flask object================
app = Flask(__name__)
app.secret_key = os.urandom(32)

#===========manage user data here====================

DB_FILE = 'data/tuesday.db'
db.create_db()

@app.route('/')
def index():
    ''' REGISTER AND LOGIN '''
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    api.checkQuote()

    quote = db.get_quote()

    return render_template('index.html', quote = quote)

@app.route('/check_user')
def check_user():
    '''CHECKS IF THE USER IS TAKEN'''
    user = request.args['user']
    if db.findUser(user):
        return 'taken'
    return 'good'

@app.route('/home')
def home():
    '''LANDING PAGE WHERE PROJECTS ARE LISTED'''
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    money = db.getUserBigcoin(username)
    return render_template('landing.html', username = session['username'], bigcoin = money)

@app.route('/profile')
def profile():
    '''PROFILE PAGE OF USER'''
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)
    money = db.getUserBigcoin(username)

    return render_template('profile.html', username = username, url = url, bigcoin = money)

@app.route('/view_profile/<project_name>/<p_id>')
def view_profile(project_name, p_id):
    '''PROFILE PAGES OF OTHER USERS'''
    if 'username' not in session:
        return redirect(url_for('index'))
    username = request.args['username']

    user_info = db.get_info(username)
    print(user_info)

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)
    print(url)

    money = db.getUserBigcoin(session['username'])

    return render_template('view_profile.html', username = username, url = url, user_info = user_info, project_name = project_name, p_id = p_id, bigcoin = money)

@app.route('/avatar')
def avatar():
    '''CUSTOMIZATION PAGE/STORE FOR YOUR AVATAR'''
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']

    eyes_price = {'eyes1':0, 'eyes10':1250, 'eyes2':1250, 'eyes3':1250, 'eyes4':1250, 'eyes6':2500, 'eyes9':2500, 'eyes5':5000, 'eyes7':5000}
    noses_price = {'nose2':0, 'nose3':1250, 'nose4':1250, 'nose5':1250, 'nose6':2500, 'nose7':2500, 'nose8':5000, 'nose9':5000}
    mouths_price = {'mouth1':0, 'mouth3':1250, 'mouth5':1250, 'mouth6':1250, 'mouth7':2500, 'mouth9':2500, 'mouth10':5000, 'mouth11':5000}
    colors_price = {'FF3333':0, 'FF3333':1250, '4DA6FF':1250, '66FF99':1250,\
                    'FFA366':1250, 'BF80FF': 2500, 'C55EB1':2500,\
                    'FFFFFF':5000, '5A6358': 5000, '000000': 5000}

    owned_eyes = db.get_value(username, 'eyes').split(',')
    owned_noses = db.get_value(username, 'noses').split(',')
    owned_mouths = db.get_value(username, 'mouths').split(',')
    owned_colors = db.get_value(username, 'color').split(',')

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)
    print(url)
    money = db.getUserBigcoin(username)

    return render_template('avatar.html', username = username, url = url, eyes = eyes_price, noses = noses_price, mouths = mouths_price, colors = colors_price,\
                            bigcoin = money, owned_eyes = owned_eyes, owned_noses = owned_noses, owned_mouths = owned_mouths, owned_colors = owned_colors)

@app.route('/purchase')
def purchase_feature():
    '''PURCHASING FEATURES FOR YOUR AVATAR'''
    '''
    USER HAS TO BE LOGGED IN TO PURCHASE FEATURE
    JS SENDS INFO TO '/purchase?feature=${feature}&value=${value}'
    NEED TO IMPLEMENT FLASK ALERT FOR SUCCESSFUL PURCHASE
    '''
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']
    bigcoin = db.getUserBigcoin(username)
    feature = request.args['feature']
    value = request.args['value']
    print(feature, value)
    if feature == 'eyes':
        eyes_price = {'eyes1':0, 'eyes10':1250, 'eyes2':1250, 'eyes3':1250, 'eyes4':1250, 'eyes6':2500, 'eyes9':2500, 'eyes5':5000, 'eyes7':5000}
        if bigcoin >= eyes_price[value]:
            price_after_purchase = bigcoin - eyes_price[value]
            db.setUserBigcoin(username, price_after_purchase)
            db.add_value(value, username, feature)
            return 'dang susan got the bread'
        else:
            return 'shucks susan lost the yeast'
    if feature == 'noses':
        noses_price = {'nose2':0, 'nose3':1250, 'nose4':1250, 'nose5':1250, 'nose6':2500, 'nose7':2500, 'nose8':5000, 'nose9':5000}
        if bigcoin >= noses_price[value]:
            price_after_purchase = bigcoin - noses_price[value]
            db.setUserBigcoin(username, price_after_purchase)
            db.add_value(value, username, feature)
            return 'dang susan got the bread'
        else:
            return 'shucks susan broke'
    if feature == 'mouths':
        mouths_price = {'mouth1':0, 'mouth3':1250, 'mouth5':1250, 'mouth6':1250, 'mouth7':2500, 'mouth9':2500, 'mouth10':5000, 'mouth11':5000}
        if bigcoin >= mouths_price[value]:
            price_after_purchase = bigcoin - mouths_price[value]
            db.setUserBigcoin(username, price_after_purchase)
            db.add_value(value, username, feature)
            return 'dang susan got the bread'
        else:
            return 'shucks susan broke'
    if feature == 'color':
        colors_price = {'FF3333':0, 'FF3333':1250, '4DA6FF':1250, '66FF99':1250,\
                        'FFA366':1250, 'BF80FF': 2500, 'C55EB1':2500,\
                        'FFFFFF':5000, '5A6358': 5000, '000000': 5000}
        if bigcoin >= colors_price[value]:
            price_after_purchase = bigcoin - colors_price[value]
            db.setUserBigcoin(username, price_after_purchase)
            db.add_value(value, username, feature)
            return 'dang susan got the bread'
        else:
            return 'shucks susan broke'


@app.route('/new_project', methods=["POST"])
def new_project():
    '''CREATES NEW PROJECT AND ENTERS INTO THE DATABASE'''
    if 'username' not in session:
        return redirect(url_for('index'))

    #data = database.DB_Manager(DB_FILE)
    print(request.form)
    projectName = request.form['newProjectName']
    if projectName.strip() == '' or '?' in projectName or '#' in projectName:
        flash('Invalid project name!')
        return redirect(url_for('home'))
    pid = str(uuid.uuid1())

    print('CREATING NEW PROJECT\n\tProject Name: {}\n\tProject ID: {}\n\tUsername: {}\n'.format(projectName, pid, session['username']))
    db.add_project(pid, session['username'], projectName)
    #data.save()

    return redirect(url_for('home'))

@app.route('/new_task', methods=['GET'])
def new_task():
    '''CREATES NEW TASK AND ENTERS INTO THE DATABASE'''
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
    return 'sad'

@app.route('/new_tmsg', methods=['GET'])
def new_team_msg():
    '''CREATES NEW TEAM MESSAGE AND ENTERS INTO THE DATABASE'''
    if 'username' not in session:
        return redirect(url_for('index'))
    print("SENDING NEW TEAM MESSAGE\n request.args: {}".format(request.args))
    pid = request.args['pid']
    user = session['username']
    msg = request.args['msg']
    msg_id = str(uuid.uuid1())
    timestamp = request.args['timestamp']
    db.add_t_msg(pid, user, msg, msg_id, timestamp)
    return 'sad'


@app.route('/join_project', methods=["POST"])
def join_project():
    '''JOINS USER TO PROJECT AND ENTERS INTO THE DATABASE'''
    if 'username' not in session:
        return redirect(url_for('index'))
    id = str(request.form['id'])
    title = db.get_project(id)
    if db.verify_project(id):
        db.add_project(id, session['username'], title)
    else:
        flash('Project ID does not exist')
    return redirect(url_for('home'))

@app.route('/project/<title>/<id>')
def project(title, id):
    '''DISPLAYS PROJECT WITH UNIQUE PROJECT ROUTE'''
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    money = db.getUserBigcoin(username)

    return render_template('project.html', username = username, project_name = title, p_id = id, bigcoin = money)

@app.route('/authenticate', methods=['POST'])

def authenticate():
    '''AUTHENTICATES THE USERNAME AND PASSWORD WHEN LOGGING IN
       VERIFIES THE INPUTTED INFORMATION WHEN REGISTERING'''
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
    '''KICKS USER OUT OF SESSION AND LOGS USER OUT'''
    if 'username' not in session:
        return redirect(url_for('index'))
    session.pop('username', None)
    flash('Successfully logged out!')
    return redirect(url_for('index'))


@app.route('/get_snippet')
def get_snippet():
    '''PULLS UP VARIOUS PIECES OF HTML FOR VARIOUS PARTS OF SITE
       DEPENDING ON REQUESTED SNIPPET (INFO SENT VIA ARGUMENT)(Joan)'''
    snippet = request.args['snippet']
    print('Getting snippet: {}'.format(snippet))

    if snippet == 'projectList' and 'username' in session:
        projectDict = db.get_projects(session['username'])
        print('Project dict: {}'.format(projectDict))
        return render_template('{}SNIPPET.html'.format(snippet), projectDict=projectDict)

    if snippet == 'privateInbox' and 'username' in session:
        username = session['username']
        pid = request.args['pid']
        private_messages = db.get_p_msgs(pid, username)
        teammates = db.get_teammates(pid)
        print(teammates)
        print('private messages', private_messages)
        msg_list = []

        for tup in private_messages:
            print('\ntup', tup)
            name = tup[1]
            eyes = db.get_current(name, 'eyes')
            nose = db.get_current(name, 'noses')
            mouth = db.get_current(name, 'mouths')
            color = db.get_current(name, 'color')
            url = api.customAvatarLink(eyes, nose, mouth, color)

            msg_list.append([tup, url])


        print('\n\n\nMESSAGE LIST\n\t{}\n\n\n'.format(msg_list))
        return render_template('{}SNIPPET.html'.format(snippet), private_messages = msg_list, teammates=teammates, username=username)

    if snippet == 'tasks' and 'username' in session:
        pid = request.args['pid']
        tasks = sorted(db.get_tasks_username(pid, session['username']), key=lambda x: x[2], reverse=True)
        unstarted = []
        workingon = []
        done = []
        for task in tasks:
            if task[4] == 0:
                unstarted.append(task)
            elif task[4] == 1:
                workingon.append(task)
            elif task[4] == 2:
                done.append(task)
        task_dict = {'unstarted': unstarted, 'workingon': workingon, 'done': done}
        print('TASK_DICT', task_dict)
        return render_template('{}SNIPPET.html'.format(snippet), task_dict = task_dict)

    if snippet == 'teamInbox' and 'username' in session:
        pid = request.args['pid']
        team_messages = db.get_t_msgs(pid)[::-1]
        print("TEAM MESSAGES:\n{}".format(team_messages))
        teammates = db.get_teammates(pid)
        teammate_pfp_urls = {}
        for mate in teammates:
            name = mate[0]
            eyes = db.get_current(name, 'eyes')
            nose = db.get_current(name, 'noses')
            mouth = db.get_current(name, 'mouths')
            color = db.get_current(name, 'color')
            teammate_pfp_urls[name] = api.customAvatarLink(eyes, nose, mouth, color)

        print('teammate_pfp_urls', teammate_pfp_urls)
        return render_template('{}SNIPPET.html'.format(snippet), pid = pid, project_name = db.get_project(pid), team_messages = team_messages, teammate_pfp_urls = teammate_pfp_urls)
    return render_template('{}SNIPPET.html'.format(snippet))

@app.route('/get_avatar')
def get_avatar():
    '''RETRIEVES AND RETURNS CURRENT USER'S AVATAR URL'''
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
    '''RETRIEVES AND RETURNS CURRENT USER'S AVATAR JSON DATA '''
    username = session['username']

    d = {}
    d['eyes'] = db.get_current(username, 'eyes')
    d['nose'] = db.get_current(username, 'noses')
    d['mouth'] = db.get_current(username, 'mouths')
    d['color'] = db.get_current(username, 'color')

    return json.dumps(d)

@app.route('/get_info')
def get_info():
    '''RETRIEVES AND RETURNS CURRENT USER'S PROFILE INFORMATION'''
    val = request.args['val']
    user = request.args['username']

    userInfo = db.get_info(user)
    pairs = ['first', 'last', 'email', 'phone', 'bio']
    return userInfo[pairs.index(val)]

@app.route('/get_username')
def get_username():
    '''RETRIEVES AND RETURNS CURRENT USER'S USERNAME INFORMATION'''
    if 'username' in session:
        return session['username']
    else:
        return 'NOT LOGGED IN'

@app.route('/get_profile_button')
def get_profile_button():
    '''CREATES PROFILE PAGE BUTTONS AND TEXT FIELDS WHEN UPDATE INFO BUTTONS CLICKED, LOADS PROFILE PAGE INFO'''
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
    '''PROCESSES INFORMATION TO BE UPDATED IN PROFILE AND ENTERS INTO DATABASE, DENIES UPDATE IF THEY DO NOT MATCH CRITERIA'''
    username = request.args['username']
    what = request.args['what']
    newVal = request.args['newVal']

    if what == 'first':
        if newVal == '':
            return "bro, that's an empty string"
        else:
            db.set_first_name(username, newVal)
    elif what == 'last':
        if newVal == '':
            return "bro, that's also an empty string"
        else:
            db.set_last_name(username, newVal)
    elif what == 'email':
        if '@' not in newVal or '.' not in newVal or len(newVal) == 0 or ' ' in newVal:
            # doesn't update if one of these things are true
            return "don't change the email"
        else:
            db.set_email(username, newVal)
    elif what == 'phone':
        if newVal.lower().islower():
            print('there are letters in this')
            return "don't change the phone number"
        else:
            db.set_phone(username, newVal)
    elif what == 'bio':
        db.set_bio(username, newVal)

    return "K we good"

@app.route('/update_avatar')
def update_avatar():
    '''ADDS A NEWLY PURCHASED FEATURE TO USER'S DATABASE ENTRY AND UPDATES CURRENT AVATAR FEATURE TO THE RECENTLY PURCHASED FEATURE'''
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
    '''GETS AVATAR FORM'''
    username = request.args['username']

    eyes = db.get_current(username, 'eyes')
    nose = db.get_current(username, 'noses')
    mouth = db.get_current(username, 'mouths')
    color = db.get_current(username, 'color')

    url = api.customAvatarLink(eyes, nose, mouth, color)
    print('GETTING AVATAR\n\tUsername: {}\n\tURL: {}\n'.format(username, url))
    print(url)
    return url

@app.route('/new_private_message')
def new_private_message():
    '''CREATES AND ADDS NEW PRIVATE MESSAGE TO THE DATABASE'''
    pid = request.args['pid']
    address = request.args['address']
    user = session['username']
    msg = request.args['msg']
    msg_id = str(uuid.uuid1())
    timestamp = request.args['timestamp']

    print("\n\n\nSENDING PM\n\n\tpid: {}\n\tto: {}\n\tfrom: {}\n\tmsg: {}\n\tmsg ID: {}\n\ttimestamp: {}\n\n\n\n".format(pid, address, user, msg, msg_id, timestamp))

    db.add_p_msg(pid, address, user, msg, msg_id, timestamp)

    return "Okie dokie!"


@app.route('/delete_private_message')
def delete_private_message():
    '''REMOVES PRIVATE MESSAGE FROM THE DATABASE'''
    msgID = request.args['msgID']
    db.remove_msg(msgID, private=1)
    return "All done here, folks!"

@app.route('/get_dashboard')
def get_dashboard():
    '''PROCESSES AND RENDERS THE DASHBOARD AND ITS COMPONENTS FOR DISPLAY'''
    username = session['username']
    pid = request.args['pid']
    project_name = db.get_project(pid)
    print("\n\n\nPID: {}\n\n\n".format(pid))

    messages = db.get_t_msgs(pid)
    print("\n\n\nPRIVATE MESSAGES:\n{}\n\n".format(messages))

    tasks = sorted(db.get_tasks_pid(pid), key=lambda x: x[2], reverse=True)

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

    else:
        done = notstarted = working = 'no tasks'

    # for team members tab thing
    teammates = db.get_teammates(pid)
    print('teammates', teammates)

    user_tasks = {}
    print('\n\n\nTEAMMATES:\n{}\n\n\n\n'.format(teammates))
    for user in teammates:
        user = user[0]
        user_tasks[user] = sorted(db.get_tasks_username(pid, user), key=lambda x: x[2], reverse=True)
        print('USER: {}\nTASKS: {}\n\n'.format(user, user_tasks[user]))

    teammate_pfp_urls = {}
    for mate in teammates:
        name = mate[0]
        eyes = db.get_current(name, 'eyes')
        nose = db.get_current(name, 'noses')
        mouth = db.get_current(name, 'mouths')
        color = db.get_current(name, 'color')
        teammate_pfp_urls[name] = api.customAvatarLink(eyes, nose, mouth, color)

    print('teammate_pfp_urls', teammate_pfp_urls)
    print("TEAMMATETASKS.ITEMS\n\n")
    for key, val in user_tasks.items():
        print("KEY: {}\nVAL: {}\n\n".format(key, val))
    print("\n\nEND")

    return render_template('dashboardSNIPPET.html', messages=messages[:5], done=str(done), working=str(working), notstarted=str(notstarted), tasks=[], teammates = teammates, username = username, teammate_pfp_urls = teammate_pfp_urls, p_id = pid, project_name = project_name, teammate_tasks=user_tasks)


@app.route('/move_task')
def move_task():
    '''CHANGES STATUS OF A TASK'''
    id = request.args['what']
    moveTo = request.args['where']

    db.set_status(int(moveTo), id)

    return "alrighty!"

@app.route('/get_data')
def get_data():
    '''GENERATES TEST DATA GIVEN INPUT PARAMETERS'''
    wc = int(request.args['wordCount'])
    sc = int(request.args['sentenceCount'])
    format = request.args['format']
    type = request.args['type']

    if type == "string":
        ipsum = api.getIpsum(wc, sc);
        if format == 'paragraph':
            ipsum = ipsum.replace('\\n', ' ')
            if ipsum[-1] == "'":
                ipsum = ipsum[:-1]
            ipsum = ' '.join(ipsum.split())
            return '"' + ipsum + '"'
        elif format == 'array':
            ipsum = [i.split() for i in ipsum.replace('.', '').split('\\n\\n')]
            for i in ipsum:
                for j in range(len(i)):
                    i[j] = '"' + i[j] + '"'
            if ipsum[-1] == ['"\'"']:
                ipsum = ipsum[:-1]
            return str(ipsum)
        else:
            return 'Invalid string format request!'
    elif type == 'integer':
        if format == 'paragraph':
            return 'That doesn\'t make sense...'
        elif format == 'array':
            out = []
            for i in range(sc):
                out.append([random.randint(0, 100) for i in range(wc)])
            return str(out)
        else:
            return 'Invalid integer format request!'

    elif type == 'float':
        if format == 'paragraph':
            return 'That doesn\'t make sense...'
        elif format == 'array':
            out = []
            for i in range(sc):
                out.append([random.random() * 100 for i in range(wc)])
            return str(out)
        else:
            return 'Invalid float format request!'

    else:
        return "Invalid type request!"


if __name__ == '__main__':
    app.debug = True
    app.run()
