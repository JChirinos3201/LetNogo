import os

from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
import datetime
import uuid # tentative

from util import db, api

app = Flask(__name__)
app.secret_key = os.urandom(32)


DB_FILE = 'data/tuesday.db'
db.create_db()

#db.add_value('eyes', 'u', 'eyes')
#db.get_current('u', 'eyes')

print(db.get_tasks("37bcd12e-181d-11e9-977f-00bb60088044", 'a'))





if __name__ == '__main__':
    app.debug = True
    app.run()

