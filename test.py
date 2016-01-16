#import os
#import urlparse
#import psycopg2
#from flask import Flask, render_template, request
#import calendar
#import time
#import collections
#import scipy.integrate
#import logging
#import datetime

#import sqlite3
#from flask import Flask, request, session, g, redirect, url_for,  abort, render_template, flash

from flask import Flask
app = Flask(__name__)
#app.config.from_object(__name__)

@app.route('/')
def home_page():
	return render_template('homepage.html')

	if __name__ == '__main__':
		app.run()