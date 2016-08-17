import sys
sys.path.insert(0, './connectors')
import sqlite_connector as connector
import data

def get_available_data(user_name):

	available_data = list()

	# todo check what data the user effectively has
	for data_id in data.get_available_data_ids():
		if connector.user_has_data(user_name, data_id):
			available_data.extend([data_id])

	return available_data

def get_data(user_name, data_id):
	# todo check data_id is valid
	return connector.get_data(user_name, data_id)

if __name__ == '__main__':

	rhrs = get_available_data("test")
	for data_id in rhrs:
		print(data.get_data_name(data_id))
