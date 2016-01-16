import os
import urlparse
import psycopg2
from flask import Flask, render_template, request
import calendar
import time
import collections
import scipy.integrate
import logging
import datetime



def get_data():
	env = get_current_event()
	totals = run_stats()
	num_entrances = len(totals.keys())
	if num_entrances != 0:
		sum_people = sum([pair[0] + pair[1] for pair in totals.values()])
		sum_ped = sum([pair[0] for pair in totals.values()])
		sum_cyc = sum([pair[1] for pair in totals.values()])

		data = []
		for location, total in totals.items():
			data.append({"loc": location, "tot": total})

		totals = {"total": str(int(sum_people * 25 / num_entrances))}
		totals["ped"] = str(int(sum_ped * 25 / num_entrances))
		totals["cyc"] = str(int(sum_cyc * 25 / num_entrances))
		return render_template("data.html", data=data, totals=totals, current={"event": env[0]})
	else:
		return render_template("data.html", data=[], totals={'total':0, 'ped':0, 'cyc':0}, current={"event": env[0]})


def create_event():
	env = get_current_event()
	if request.method == "GET":
		return render_template('create_event.html')
	else:
		conn = connect_postgres()
		cur = conn.cursor()

		epoch_starttime = time.mktime(datetime.datetime.strptime(request.form['event-starttime'], "%Y-%m-%dT%H:%M").timetuple())
		epoch_endtime = time.mktime(datetime.datetime.strptime(request.form['event-endtime'], "%Y-%m-%dT%H:%M").timetuple())

		cur.execute("INSERT INTO events (start_time, end_time, location, count_interval, entrances) VALUES (%s,%s,%s,%s,%s)",
			(epoch_starttime, epoch_endtime, request.form['event-name'], 900, request.form['event-entrances']))
		conn.commit()
		events = []
		cur.execute("SELECT * FROM events;")
		for event in cur.fetchall():
			events.append({"data": event})
		end_postgres(conn, cur)
		return render_template('select_event.html', events=events, data={"event": env[0]}, add={'add': False})



def post_to_postgres(num_people, num_bikes, loc):
	env = get_current_event()
	conn = connect_postgres()
	cur = conn.cursor()

	cur.execute("INSERT INTO sessions (eid, time, location, count_people, count_bikes) VALUES (%s,%s,%s,%s,%s)", 
		(env[0], calendar.timegm(time.gmtime()), loc, num_people, num_bikes))
	conn.commit()
	end_postgres(conn, cur)
