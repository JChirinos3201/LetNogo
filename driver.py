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

print(db.add_t_msg('50ea662a-1908-11e9-b3fa-00bb60088044', 'sus', 'Yo guys she needs help', '0', '0000'))
#print(db.remove_t_msg('0'))
print(db.get_t_msgs('50ea662a-1908-11e9-b3fa-00bb60088044'))



if __name__ == '__main__':
    app.debug = True
    app.run()

