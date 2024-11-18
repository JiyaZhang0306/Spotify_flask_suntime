import spotipy
import json
import webbrowser
import urllib.request
import spotipy.util as util

# weather_file is a variable name representing my file
with open('weather_key.txt', 'r') as weather_file:
    weather_key = weather_file.read()

with open('spotify_keys.json', 'r') as spotify_file:
    # load reads a JSON string from a file
    tokens = json.load(spotify_file)


my_client_id = tokens['client_id']
my_client_secret = tokens['client_secret']
redirectURI = tokens['redirect']
username = tokens['username']

scope = "user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public"
token = util.prompt_for_user_token(username, scope, client_id=my_client_id, client_secret=my_client_secret, redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)

def get_playlist(city):
	url = f"http://api.weatherapi.com/v1/current.json?key={weather_key}&q={city}&aqi=no"

	# sending our url to the interwebs
	request = urllib.request.Request(url)
	# capture all the JSON coming back from the interwebs
	response = urllib.request.urlopen(request)
	weather_json = json.loads(response.read())

	forecast = weather_json['current']['condition']['text']

	track_results = sp.search(q=forecast, type='track', limit=50)
	song_data = track_results['tracks']['items']

	song_uris = []

	for song in song_data:
	    song_uris.append(song['uri'])

	my_playlist = sp.user_playlist_create(user=username, name=forecast, public=True, description="songs for the weather")
	sp.user_playlist_add_tracks(username, my_playlist['id'], song_uris)

	return my_playlist['id']