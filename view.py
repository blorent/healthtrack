from flask import render_template, request
from pandas_highcharts.core import serialize, _pd2hc_kind
import pandas
import model
import logging
import os

# Available types : "bar": "column", "barh": "bar", "area": "area", "line": "line", "pie": "pie"
# Expects a Pandas serie
def gen_highcharts_json(data, title, x_axis=None, kind='line', pandas_highcharts=True):

	if pandas_highcharts:
		json = serialize(data.to_frame(), output_type='json', title=title, kind=kind, fontsize='12', grid=True, legend=False)
	else:
		# define index type
		if data.index.dtype == 'datetime64[ns]':
			x_axis_type = 'datetime'
		else:
			x_axis_type = 'category'

		print(x_axis_type)

		json = """{
	title: {
		text: '"""+title+"""'
	},
	xAxis: {
		type: '"""+x_axis_type+"""',
		dateTimeLabelFormats: {
				month: '%e. %b',
				year: '%b'
		},
		title: {
			text: 'Date'
		}
	},
	yAxis: {
		title: {
			text: '"""+title+"""'
		}
	},
	legend: {
		enabled: false
	},
	credits: false,
	plotOptions: {
		line: {
			marker: {
				enabled: null,
				radius: 3
			},
			lineWidth: 2,
			states: {
				hover: {
					lineWidth: 2
				}
			},
			threshold: null
		}
	},
	series: [{
		type : '"""+kind+"""',
		data: ["""
		for index, value in data.iteritems():
			if x_axis_type == 'datetime':
				json += '[Date.UTC({}, {}, {}),{}],'.format(str(index)[0:4], str(index)[5:7], str(index)[8:10], value)
			else:
				json += '["{}",{}],'.format(str(index), value)
		json = json[:-1]
		json+= """]
	}]
}
	"""

	#print(json)

	return json


def show_health_data(health_data):
	highcharts_json = gen_highcharts_json(health_data, 'RHR', kind='spline', pandas_highcharts=False)
	return render_template('log.html', chart='my-chart', highcharts_code=highcharts_json)

