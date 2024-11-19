import spotipy
import json
import webbrowser
import urllib.request
import spotipy.util as util

import gmplot
import os
import requests
import googlemaps

from datetime import datetime, timedelta

# get google map key
with open("googlemap_key.txt", "r") as file:
    googlemap_key = file.read()

map_client = googlemaps.Client(googlemap_key)

ip_address = requests.get('https://api.ipify.org').text
url_map = f"https://ipinfo.io/{ip_address}/json"
request_map = urllib.request.Request(url_map)
response_map = urllib.request.urlopen(request_map)
location_json = json.loads(response_map.read())
lattitude, longtitude = location_json['loc'].split(',')
print(f"Latitude: {lattitude}, Longitude: {longtitude}")

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

def add_tracks_to_playlist(playlist_id, uris):
    if uris:
        sp.user_playlist_add_tracks(username, playlist_id, uris)
        print(f"Added {len(uris)} tracks to playlist {playlist_id}.")
    else:
        print(f"No URIs provided. Skipping track addition for playlist {playlist_id}.")

def calculate_time_difference(ip_lat, ip_lng, city_lat, city_lng):
    #Calculate the time difference in hours between the IP city and input city.

    # Get timezone information for IP location
    ip_timezone = map_client.timezone((ip_lat, ip_lng))
    ip_offset_seconds = ip_timezone['rawOffset'] + ip_timezone['dstOffset']
    ip_offset_hours = ip_offset_seconds / 3600  # Convert seconds to hours

    # Get timezone information for the input city
    city_timezone = map_client.timezone((city_lat, city_lng))
    city_offset_seconds = city_timezone['rawOffset'] + city_timezone['dstOffset']
    city_offset_hours = city_offset_seconds / 3600  # Convert seconds to hours

    # Calculate the time difference
    time_difference = city_offset_hours - ip_offset_hours
    print(f"Time difference (input city - IP city): {time_difference} hours")
    return time_difference

def get_sunrise_playlist(city):

    # Geocode city
    response_hometown_map = map_client.geocode(city)
    hometown_latitude = response_hometown_map[0]['geometry']['location']['lat']
    hometown_longitude = response_hometown_map[0]['geometry']['location']['lng']
    print(f"Hometown Latitude: {hometown_latitude}, Longitude: {hometown_longitude}")

    # Get sunrise and sunset times
    url = f"https://api.sunrise-sunset.org/json?lat={lattitude}&lng={longtitude}"
    url_hometown = f"https://api.sunrise-sunset.org/json?lat={hometown_latitude}&lng={hometown_longitude}"

    suntime_json = json.loads(urllib.request.urlopen(urllib.request.Request(url)).read())
    hometown_suntime_json = json.loads(urllib.request.urlopen(urllib.request.Request(url_hometown)).read())

    sunrise = suntime_json['results']['sunrise']
    sunrise_hometown = hometown_suntime_json['results']['sunrise']
    format_str = "%I:%M:%S %p"
    sunrise_dt = datetime.strptime(sunrise, format_str)
    sunrise_hometown_dt = datetime.strptime(sunrise_hometown, format_str)

    if sunrise_dt < sunrise_hometown_dt:
        sunrise_dt += timedelta(days=1)

    time_difference = calculate_time_difference(lattitude, longtitude, hometown_latitude, hometown_longitude)

    sunrise_time_difference = sunrise_dt - sunrise_hometown_dt
    sunrise_mood = sunrise_time_difference.total_seconds() / 3600 - time_difference

    # Fetch tracks
    playlist_id = '5ABHKGoOzxkaa28ttQV9sE'
    track_results = sp.playlist(playlist_id)
    song_data = track_results['tracks']['items']
    songs_id = [song['track']['id'] for song in song_data]
    song_feature = sp.audio_features(songs_id)

    sunrise_matching_songs = [
        song for song in song_feature if round(song.get('valence', 0), 1) == round(abs(sunrise_mood), 1)
    ]
    sunrise_song_uris = [song['uri'] for song in sunrise_matching_songs]

    # Create playlist and add tracks
    my_sunrise_playlist = sp.user_playlist_create(user=username, name="Sunrise Playlist", public=True, description="Songs for the sunrise")
    print(f"Sunrise Playlist ID: {my_sunrise_playlist['id']}")
    add_tracks_to_playlist(my_sunrise_playlist['id'], sunrise_song_uris)

    return my_sunrise_playlist['id']


def get_sunset_playlist(city):

    response_hometown_map = map_client.geocode(city)
    hometown_latitude = response_hometown_map[0]['geometry']['location']['lat']
    hometown_longitude = response_hometown_map[0]['geometry']['location']['lng']

    url = f"https://api.sunrise-sunset.org/json?lat={lattitude}&lng={longtitude}"
    url_hometown = f"https://api.sunrise-sunset.org/json?lat={hometown_latitude}&lng={hometown_longitude}"

    suntime_json = json.loads(urllib.request.urlopen(urllib.request.Request(url)).read())
    hometown_suntime_json = json.loads(urllib.request.urlopen(urllib.request.Request(url_hometown)).read())

    sunset = suntime_json['results']['sunset']
    sunset_hometown = hometown_suntime_json['results']['sunset']
    format_str = "%I:%M:%S %p"
    sunset_dt = datetime.strptime(sunset, format_str)
    sunset_hometown_dt = datetime.strptime(sunset_hometown, format_str)

    if sunset_dt < sunset_hometown_dt:
        sunset_dt += timedelta(days=1)

    time_difference = calculate_time_difference(lattitude, longtitude, hometown_latitude, hometown_longitude)

    sunset_time_difference = sunset_dt - sunset_hometown_dt
    sunset_mood = sunset_time_difference.total_seconds() / 3600 - time_difference

    playlist_id = '37i9dQZF1DXcBWIGoYBM5M'
    track_results = sp.playlist(playlist_id)
    song_data = track_results['tracks']['items']
    songs_id = [song['track']['id'] for song in song_data]
    song_feature = sp.audio_features(songs_id)

    sunset_matching_songs = [
        song for song in song_feature if round(song.get('valence', 0), 1) == round(abs(sunset_mood), 1)
    ]
    sunset_song_uris = [song['uri'] for song in sunset_matching_songs]

    my_sunset_playlist = sp.user_playlist_create(user=username, name="Sunset Playlist", public=True, description="Songs for the sunset")
    print(f"Sunset Playlist ID: {my_sunset_playlist['id']}")
    add_tracks_to_playlist(my_sunset_playlist['id'], sunset_song_uris)

    return my_sunset_playlist['id']