import spotipy
import json
import webbrowser
import urllib.request
import spotipy.util as util

#imoort google map
import gmplot
import os
import requests
import googlemaps

from datetime import datetime, timedelta

# get google map key
with open("googlemap_key.txt", "r") as file:
    googlemap_key = file.read()

map_client = googlemaps.Client(googlemap_key)

#google api url to get location for suntime api
#get another city's location for suntime2
ip_address = requests.get('https://api.ipify.org').text
hometown_address = 'Minto,Canada'

#get home town address information
response_hometown_map = map_client.geocode(hometown_address)
print(response_hometown_map)

hometown_lattitude = response_hometown_map[0]['geometry']['location']['lat']
hometown_longtitude = response_hometown_map[0]['geometry']['location']['lng']
print(hometown_lattitude)
print(hometown_longtitude)

url_map = f"https://ipinfo.io/{ip_address}/json"

request_map = urllib.request.Request(url_map)
response_map = urllib.request.urlopen(request_map)

location_json = json.loads(response_map.read())

lattitude, longtitude = location_json['loc'].split(',')


#use google map current location to get suntime api
url = f"https://api.sunrise-sunset.org/json?lat={lattitude}&lng={longtitude}"


#get hometown's suntime information
url_hometown = f"https://api.sunrise-sunset.org/json?lat={hometown_lattitude}&lng={hometown_longtitude}"

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

#hometown
request_hometown = urllib.request.Request(url_hometown)
response_hometown = urllib.request.urlopen(request_hometown)

type(response)
type(response_hometown)

suntime_json = json.loads(response.read())

hometown_suntime_json = json.loads(response_hometown.read())

sunrise_hometown = hometown_suntime_json['results']['sunrise']
sunset_hometown = hometown_suntime_json['results']['sunset']

# the printed time is in UK time(8hrs difference)
print(sunrise_hometown)
print(sunset_hometown)

sunrise = suntime_json['results']['sunrise']
sunset = suntime_json['results']['sunset']

print(sunrise)
print(sunset)

# suntime difference

#sunrise
format_str = "%I:%M:%S %p"
sunrise_hometown_dt = datetime.strptime(sunrise_hometown, format_str)
sunrise_dt = datetime.strptime(sunrise, format_str)

if sunrise_dt < sunrise_hometown_dt:
    sunrise_dt += timedelta(days=1)

sunrise_time_difference = sunrise_dt - sunrise_hometown_dt
sunrise_difference = sunrise_time_difference.total_seconds() / 3600  # Convert seconds to hours
print(sunrise_difference)

#sunset
format_str = "%I:%M:%S %p"
sunset_hometown_dt = datetime.strptime(sunset_hometown, format_str)
sunset_dt = datetime.strptime(sunset, format_str)

if sunset_dt < sunset_hometown_dt:
    sunset_dt += timedelta(days=1)

sunset_time_difference = sunset_dt - sunset_hometown_dt
sunset_difference = sunset_time_difference.total_seconds() / 3600  # Convert seconds to hours
print(sunset_difference)

#time difference set the style of music?
#use numbers after the point, to decide the mood
sunrise_mood = sunrise_difference - 18
print(sunrise_mood)

sunset_mood = sunset_difference - 18
print(sunset_mood)

# open spotify api
#ignore the key in git
with open('spotify_keys.json', 'r') as spotify_file:
    tokens = json.load(spotify_file)

client_id = tokens['client_id']
client_secret = tokens['client_secret']
redirectURI = tokens['redirect']
username = tokens['username']


scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public user-top-read user-library-read user-read-recently-played'
token = util.prompt_for_user_token(username, scope, client_id=client_id,
                           client_secret=client_secret,
                           redirect_uri=redirectURI)

sp = spotipy.Spotify(auth=token)

playlist_id = '5ABHKGoOzxkaa28ttQV9sE'
track_results = sp.playlist(playlist_id)
print(track_results)

song_data = track_results['tracks']['items']
print(song_data)

songs_id = []
for song in song_data:
    songs_id.append(song['track']['id'])   

song_feature = sp.audio_features(list(songs_id))
print(song_feature)

song_valence = []

for song in song_feature:
    song_valence.append(song['valence'])   


sunrise_matching_songs = [song for song in song_feature if round(song.get('valence'),1) == round(abs(sunrise_mood),1)]
sunset_matching_songs = [song for song in song_feature if round(song.get('valence'),1) == round(abs(sunset_mood),1)]
print(sunrise_matching_songs)
print(sunset_matching_songs)

playlist_id = '37i9dQZEVXbKj23U1GF4IR'
hometown_playlist_tracks = sp.playlist(playlist_id)
print(hometown_playlist_tracks)

hometown_song_data = hometown_playlist_tracks['tracks']['items']
print(hometown_song_data)


hometown_id = []
for song in hometown_song_data:
    hometown_id.append(song['track']['id'])   


hometown_feature = sp.audio_features(list(hometown_id))

# find valence in song_feature which = sunrise_mood
hometown_sunrise_matching_songs = [song for song in hometown_feature if round(song.get('valence'),1) == round(abs(sunrise_mood),1)]
hometown_sunset_matching_songs = [song for song in hometown_feature if round(song.get('valence'),1) == round(abs(sunset_mood),1)]

sunrise_song_uris = []
for song in sunrise_matching_songs:
    sunrise_song_uris.append(song['uri'])
    
for song in hometown_sunrise_matching_songs:
    sunrise_song_uris.append(song['uri'])

my_sunrise_playlist = sp.user_playlist_create(user=username, name=sunrise, public=True, description="songs for the sunrise")

sunset_song_uris = []
for song in sunset_matching_songs:
    sunset_song_uris.append(song['uri'])
    
for song in hometown_sunset_matching_songs:
    sunset_song_uris.append(song['uri'])


my_sunset_playlist = sp.user_playlist_create(user=username, name=sunset, public=True, description="songs for the sunset")

sp.user_playlist_add_tracks(username, my_sunrise_playlist['id'], sunrise_song_uris)

sp.user_playlist_add_tracks(username, my_sunset_playlist['id'], sunset_song_uris)

webbrowser.open(my_sunrise_playlist['external_urls']['spotify'])
webbrowser.open(my_sunset_playlist['external_urls']['spotify'])