import spotipy
import spotipy.util as util
import json
import time
import requests

from flask import Flask, render_template, request
from suntime_spotify import get_sunrise_playlist, get_sunset_playlist

# Load Spotify API keys
with open('spotify_keys.json', 'r') as spotify_file:
    tokens = json.load(spotify_file)

client_id = tokens['client_id']
client_secret = tokens['client_secret']
redirectURI = tokens['redirect']
username = tokens['username']
scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-top-read user-library-read user-read-recently-played'

def get_refresh_token():

    token_info = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    print(f"Access Token: {token_info}")
    print("Save the refresh token for future use.")


if __name__ == "__main__":
    authenticate_spotify()  # Authenticate initially to get tokens
    # Run your Flask app or other logic here

app = Flask(__name__)

default_city = 'Minto, Canada'

@app.route('/', methods=['GET', 'POST'])
def index():
    city = default_city
    sunrise_playlist_id = ""
    sunset_playlist_id = ""

    if request.method == 'POST':
        city = request.form['req_city']

        # Generate both playlists based on user input
        sunrise_playlist_id = get_sunrise_playlist(city)
        sunset_playlist_id = get_sunset_playlist(city)

    return render_template(
        'index.html',
        city=city,
        sunrise_playlist_id=sunrise_playlist_id,
        sunset_playlist_id=sunset_playlist_id
    )

if __name__ == '__main__':
    app.run(debug=True)