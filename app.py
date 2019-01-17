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

@app.route('/check_user')
def check_user():
    user = request.args['user']
    if db.findUser(user):
        return 'taken'
    return 'good'

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    money = db.getUserBigcoin(username)
    return render_template('landing.html', username = session['username'], bigcoin = money)

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
    money = db.getUserBigcoin(username)

    return render_template('profile.html', username = username, url = url, bigcoin = money)

@app.route('/view_profile/<project_name>/<p_id>')
def view_profile(project_name, p_id):
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

    return render_template('view_profile.html', username = username, url = url, user_info = user_info, project_name = project_name, p_id = p_id, bigcoin = money)

@app.route('/avatar')
def avatar():
    if 'username' not in session:
        return redirect(url_for('index'))
    username = session['username']

    eyes_price = {'eyes1':0, 'eyes10':1250, 'eyes2':1250, 'eyes3':1250, 'eyes4':1250, 'eyes6':2500, 'eyes9':2500, 'eyes5':5000, 'eyes7':5000}
    noses_price = {'nose2':0, 'nose3':1250, 'nose4':1250, 'nose5':1250, 'nose6':2500, 'nose7':2500, 'nose8':5000, 'nose9':5000}
    mouths_price = {'mouth1':0, 'mouth3':1250, 'mouth5':1250, 'mouth6':1250, 'mouth7':2500, 'mouth9':2500, 'mouth10':5000, 'mouth11':5000}
    colors_price = {'yellow':('FFFF33', 0), 'red':('FF3333', 1250), 'blue': ('4DA6FF', 1250), 'green':('66FF99', 1250),\
                    'orange':('FFA366', 1250), 'purple':('BF80FF', 2500), 'pink':('C55EB1', 2500),\
                    'white':('FFFFFF', 5000), 'grey':('5A6358', 5000), 'black':('000000', 5000)}

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
        colors_price = {'yellow':('FF3333', 0), 'red':('FF3333', 1250), 'blue': ('4DA6FF', 1250), 'green':('66FF99', 1250),\
                        'orange':('FFA366', 1250), 'purple':('BF80FF', 2500), 'pink':('C55EB1', 2500),\
                        'white':('FFFFFF', 5000), 'grey':('5A6358', 5000), 'black':('000000', 5000)}
        if bigcoin >= colors_price[value][1]:
            price_after_purchase = bigcoin - colors_price[value][1]
            db.setUserBigcoin(username, price_after_purchase)
            db.add_value(value, username, feature)
            return 'dang susan got the bread'
        else:
            return 'shucks susan broke'


@app.route('/new_project', methods=["POST"])
def new_project():
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
    if 'username' not in session:
        return redirect(url_for('index'))
    print(request.args)
    pid = request.args['pid']
    user = session['username']
    msg = request.args['msg']
    msg_id = str(uuid.uuid1())
    timestamp = request.args['time']
    db.add_t_msg(pid, user, msg, msg_id, timestamp)
    return 'sad'


@app.route('/join_project', methods=["POST"])
def join_project():
    '''
    user joins a project
    '''
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
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    money = db.getUserBigcoin(username)

    return render_template('project.html', username = username, project_name = title, p_id = id, bigcoin = money)

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
        private_messages = db.get_p_msgs(pid)
        teammates = db.get_teammates(pid)
        print(teammates)
        print(private_messages)
        username = session['username']
        msg_list = []
        for tup in private_messages:
            if tup[0] == username:
                l = list(tup)
                name = tup[1]
                eyes = db.get_current(name, 'eyes')
                nose = db.get_current(name, 'noses')
                mouth = db.get_current(name, 'mouths')
                color = db.get_current(name, 'color')
                url = api.customAvatarLink(eyes, nose, mouth, color)
                msg_list += [i for i in private_messages] + [url]

        print('MESSAGE LIST\n\t{}\n\n\n'.format(msg_list))
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
        team_messages = db.get_t_msgs(pid)
        print(team_messages)
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
        return render_template('{}SNIPPET.html'.format(snippet), team_messages = team_messages, teammate_pfp_urls = teammate_pfp_urls)
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
        if '@' not in newVal or '.' not in newVal:
            # do something here helppppppppppppppppppppppppppppppppppppp
            return 'nou'
        else:
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

@app.route('/new_private_message')
def new_private_message():
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
    msgID = request.args['msgID']
    db.remove_msg(msgID, private=1)
    return "All done here, folks!"

@app.route('/get_dashboard')
def get_dashboard():
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
    id = request.args['what']
    moveTo = request.args['where']

    db.set_status(int(moveTo), id)

    return "alrighty!"










if __name__ == '__main__':
    app.debug = True
    app.run()
