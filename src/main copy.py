import requests

from auth import Auth
import json
import numpy as np
import pandas as pd

base_url = 'https://api.spotify.com/v1/'

auth = Auth()
token = auth.get_token()

headers = {
    'Authorization': f'Bearer {token}',
    "Accept": "application/json"
}

#search = "album:Blackstar"
#search = search.replace(' ', r'%20')

# params = {
#     'type' : "album",
#     'q' : search
# }
params = {
    'time_range' : 'medium_term',
    'limit' : 10,
    'offset' : 5
}

response = json.loads(requests.get(base_url+"me/top/tracks", headers=headers, params=params).content)
print(response)

def get_top_tracks(response):
    top_tracks = [ response["items"][i]["name"] for i in range(len(response["items"])) ]
    return top_tracks

def get_top_tracks_artists(response):
    artists = [response["items"][i]["artists"] for i in range(len(response["items"])) ]
    songs = [ response["items"][i]["name"] for i in range(len(response["items"])) ]
    dict_artists = dict(zip(songs, artists))
    for song in dict_artists.keys():
        list_artists = []
        for artist in dict_artists[song]:
            list_artists.append(artist["name"])
        dict_artists[song] = list_artists
    return dict_artists

if response:
    print(get_top_tracks(response))
    print(get_top_tracks_artists(response))
else:
    print(f"Error {response.status_code}")
    print(response.content)