from flask import Flask, render_template, request
from weather_spotify import get_playlist

# app is a variable representing 
# our flask app
# __name__ is a python reserved 
# word
# telling Flask where our code
# lives
app = Flask(__name__)

default_city = 'London'

# set up our landing page
@app.route('/')
def index():
	my_playlist = get_playlist(default_city)
	return render_template('index.html', playlist_id=my_playlist, city=default_city)

# only use this when posting data!
@app.route('/', methods=['POST'])
def index_post():
	user_city = request.form['req_city']
	my_playlist = get_playlist(user_city)
	return render_template('index.html', playlist_id=my_playlist, city=user_city)