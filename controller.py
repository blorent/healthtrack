import logging, os, model, view
from flask import Flask

app = Flask(__name__)

# Set up logging for everyone
def configure_logger():

    # Log to file
    logging.basicConfig(filename='healthtrack.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


# Controller calls View
@app.route('/user/<username>/log')
def log(username):
	health_data = model.get_data(username, 1)
	return view.show_health_data(health_data)

if __name__ == '__main__':

	configure_logger()
	app.run(debug=True)