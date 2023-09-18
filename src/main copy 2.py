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

response = json.loads(requests.get(base_url+"playlists/37i9dQZF1DWWGFQLoP9qlv", headers=headers, params=params).content)
def get_tracks(response_playlist):
    id_tracks = [response_playlist["tracks"]["items"][i]["href"].split[-1] for i in range(len(response_playlist["tracks"]["items"]))]

    return id_tracks

if response:
    print(response["tracks"].keys() )
    print(get_tracks(response))

else:
    print(f"Error {response.status_code}")
    print(response.content)