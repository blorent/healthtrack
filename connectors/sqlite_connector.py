import sqlite3 as lite
from datetime import datetime, timedelta
import os
import pandas as pd
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import data
from random import randrange

database_name = "data/healthtrack_sqlite3.db"

def create_database():
	with lite.connect(database_name) as con:
		cur = con.cursor()
		cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, birthdate DATETIME, level INT)")
		for data_id in data.get_available_data_ids():
			cur.execute("CREATE TABLE {}(id INTEGER PRIMARY KEY, date_measured TIMESTAMP, user_id INT, value INT)".format(data.get_table_name(data_id)))

def insert_test_data():
	with lite.connect(database_name) as con:
		cur = con.cursor()
		print("INSERT INTO users(id, name, birthdate, level) VALUES(1, 'test', '{}', 8)".format(datetime(1985, 2, 2)))
		cur.execute("INSERT INTO users(id, name, birthdate, level) VALUES(1, 'test', '{}', 8)".format(datetime(1985, 2, 2)))


		for data_id in data.get_available_data_ids():
			values_range = data.get_data_range(data_id)
			values = (
				(datetime.now() - timedelta(days=9), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=8), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=7), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=6), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=5), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=4), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=3), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=2), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=1), 1, randrange(values_range[0], values_range[1])),
				(datetime.now() - timedelta(days=0), 1, randrange(values_range[0], values_range[1])))

			cur.executemany("INSERT INTO {}(date_measured, user_id, value) VALUES(?, ?, ?)".format(data.get_table_name(data_id)), values)


def get_user_id(user_name):
	with lite.connect(database_name) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM users WHERE name='{}'".format(user_name))
		rows = cur.fetchall()
		if len(rows) == 0:
			raise ValueError("Invalid user name")
		elif len(rows) > 1:
			raise ValueError("Mulitple users with name={}".format(user_name))
		else:
			return rows[0][0]

def user_has_data(user_name, data_id):

	table_name = data.get_table_name(data_id)
	user_id = get_user_id(user_name)
	with lite.connect(database_name) as con:
		cur = con.cursor()
		cur.execute("SELECT * FROM {} WHERE user_id={}".format(table_name, user_id))
		rows = cur.fetchall()
		return len(rows) != 0


def get_data(user_name, data_id):

	con = lite.connect(database_name)
	user_id = get_user_id(user_name)
	if not user_has_data(user_name, data_id):
		return None
	df = pd.read_sql_query("SELECT * FROM {} WHERE user_id={}".format(data.get_table_name(data_id), user_id), con)
	if df.empty:
		return None
	df.set_index('date_measured', inplace=True)
	con.close()

	# Convert date index to proper datetime
	df.value.index = pd.to_datetime(df.value.index)
	return df.value

def insert_data(user_name, data_name, measurement_date, value):
	con = lite.connect(database_name)
	user_id = get_user_id(user_name)
	with con:
		cur = con.cursor()
		cur.execute("INSERT INTO {} VALUES({}, {}, {})".format(data_name, measurement_date, user_id, value))
		con.close()



if __name__ == '__main__':
	if os.path.exists(database_name):
		os.remove(database_name)
	create_database()
	insert_test_data()
	data = get_data("test", "resting_heart_rate")
	print(data.index)
	data.index = pd.to_datetime(data.index)
	print(data.index)