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

#db.add_t_msg('50ea662a-1908-11e9-b3fa-00bb60088044', 'sus', 'Yo guys she needs help', '0', '0000')
#print(db.add_t_msg('50ea662a-1908-11e9-b3fa-00bb60088044', 'sus', 'More help!!', '1', '1111'))
#print(db.remove_t_msg('0'))
#print(db.get_t_msgs('50ea662a-1908-11e9-b3fa-00bb60088044'))

#db.setUserBigcoin('sus', 0)
#set_status(status, taskID)
#db.add_task('473b1c96-19c1-11e9-b907-00bb60088044', 'sus', 'Macking people', 'macking more', '0', '2002-12-12', '0')
#db.set_priority(2, '7e798350-19d5-11e9-a2c2-00bb60088044')
db.set_status(2, '4d3572d8-19d8-11e9-80a9-00bb60088044')


if __name__ == '__main__':
    app.debug = True
    app.run()

