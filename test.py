import os
#import urlparse
#import psycopg2
#from flask import Flask, render_template, request
import calendar
import time
#import collections
#import scipy.integrate
#import logging
import datetime
import sqlite3
from flask import Flask, request, session, g, redirect, url_for,  abort, render_template, flash

from contextlib import closing

DATABASE = 'riceuber.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/data')
def data():
	return render_template('data.html')


####

def connect_db():
    print("connect_db")
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    print("before_request")
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def executeScriptsFromFile(filename, a):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        #try:
        a.execute(command)
        #except OperationalError, msg:
        #    print "Command skipped: ", msg


#######

@app.route('/addride/', methods=['GET', 'POST'])
def add_ride():
	
	if request.method == "GET":
		return render_template('addride.html')
	else:
		c = g.db.cursor()
		epoch_time = time.mktime(datetime.datetime.strptime(request.form['datetime'], "%Y-%m-%dT%H:%M").timetuple())

		executeScriptsFromFile('schema.sql',c)

		c.execute('INSERT INTO entries (name, email, phone, datetime, fromloc, toloc) VALUES (?, ?, ?, ?, ?, ?)', (request.form['name'], request.form['email'], request.form['phone'], epoch_time, request.form['fromloc'], request.form['toloc']))
		g.db.commit()
		rides = []
		c.execute("SELECT * FROM entries;")
		for entry in c.fetchall():
			rides.append({"data": entry})
		
		return render_template('data.html')
		#events=events, data={"event": env[0]}, add={'add': False}
######



if __name__ == '__main__':
    app.run(host=None, port=8080)
