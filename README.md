# Team LetNogo
# Project Tuesday
#### By Joan Chirinos, Susan Lin, Johnny Wong, and Thomas Zhao

Project managing website. Projects can be created and can be shared with other members. Members can send out the project ID for other teammates to search up and join. When teammates join, tasks may be delegated. Once a task is assigned or added, the user’s feed will update. Each member will also be able to comment on the completeness of their tasks (not started, working on it, done, etc.)

The database will have tables for login info, projects, tasks, etc.

There may be a messaging system which allows teammates to “comment” on work, much like how “reactions” work on Facebook. There would NOT be a reply system in order to encourage face-to-face communication; i.e. the messaging system is solely for quick comments and should be limited to very few words/characters (like 140 character tweets, but possibly shorter).

We are displaying motivational quotes and avatars for the user simply to enhance the user experience. We are also using the Dino Ipsum API to generate strings for testing code, or just as an all-purpose lorem ipsum generator for web-based projects.

## How to Run:
#### Create a Virtual Environment
Using a venv is important in order to create a isolated Python environment to run code with specific dependencies exclusive to the venv and not globally. 

__To create a venv...__
1. In a terminal, navigate to the directory you want to keep your venv (eg. `cd ~/<venv_dir>`)
2. Run `python3 -m venv <venv_name>` (replace `<venv_name>` with whatever name you'd like) 
3. Activate your virtual environment by running `source <venv_name>/bin/activate`
4. Your computer's name should be preceeded by `(venv_name)` now. You are inside your virtual environment.
5. You can deactivate your venv by running the command `deactivate`
6. You can activate the venv from any current working directory by running `source ~/venv_name/bin/activate`

#### Install Dependencies
After activating the virtual environment:
Install our __dependencies__ with `pip install -r <path-to-file>requirements.txt`

#### Run _Tuesday_
1. Run `python app.py`
2. Open `localhost:5000` in a browser

## API Information
We are utilizing __3__ APIs in this project. See below for more information.

### [Quotes API](http://quotes.rest/)
* __NO KEYS__ :heart_eyes: required for this API
* Used to return motivational quotes at our login/register page! 
* Limited to 10 requests/hr 

If the limit is reached, we return our own motivational quote :smirk:

### [Dino Ipsum API](http://dinoipsum.herokuapp.com/)
* __NO KEYS__ :heart_eyes: required for this API
* Returns a Dino Ipsum we can use to generate strings or as an all-purpose lorem ipsum generator

### [Adorable Avatars API](https://avatars.adorable.io/)
* __NO KEYS__ :heart_eyes: required for this API
* Adorable Avatars is the bad boy that generates our unique profile avatars for each user.
* Provides several options for eyes, noses, mouths
* Users are able to unlock more options by spending currency :dollar: that they'd earn by contributing to projects on our website :relieved:

## Dependencies
### Python 3
We are using Python 3 as our primary language to facilitate scripting and to utilize the dependencies below.
We use the following __modules__:
1. __datetime__ (provides a timestamp for messaging)
2. __json__ & __request__ (to request information from our APIs)
3. __random__ (to select a random motivational quote)
4. __sqlite3__ (to utilize our sqlite3 database `tuesday.db`)
5. __uuid__ (to create unique identifiers for projects and messages)
6. __os__ (to create _Flask_ secret keys)

### Other dependencies
- __Wheel__
- __Flask__ (manages our server handling)



