import sqlite3
from flask import Flask, request, session, g, redirect, url_for,  abort, render_template, flash


DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home_page():
    return render_template('homepage.html')

@app.route('/addride')
def add_ride():
	pass

@app.route('/data')
def data():
	pass


if __name__ == '__main__':
    app.run()
