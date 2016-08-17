data_id_to_data_name = {
1:"Resting Heart Rate",
2:"SPO2",
3:"Weight",
4:"Body Fat"
}

data_id_to_table_name = {
1:"resting_heart_rate",
2:"spo2",
3:"weight",
4:"body_fat"
}

data_typical_range = {
1:[35, 70],
2:[95, 99],
3:[50,90],
4:[4, 25]
}

def get_available_data_ids():
	return data_id_to_data_name.keys()

def get_data_name(data_id):
	if not data_id in data_id_to_data_name:
		raise ValueError("Invalid data ID")

	return data_id_to_data_name[data_id]

def get_table_name(data_id):
	if not data_id in data_id_to_table_name:
		raise ValueError("Invalid data ID")

	return data_id_to_table_name[data_id]

def data_name_to_table_name(data_name):
	for key,val in data_id_to_data_name.iteritems():
		if val == data_name:
			return data_id_to_table_name[key]

	raise ValueError("Data name does not exist")

def table_name_to_data_name(table_name):
	for key,val in data_id_to_table_name.iteritems():
		if val == table_name:
			return data_id_to_data_name[key]

	raise ValueError("Data name does not exist")

def get_data_range(data_id):
	if not data_id in data_typical_range:
		raise ValueError("Invalid data ID")

	return data_typical_range[data_id]