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
    'limit' : 1,
    'offset' : 5
}

response = json.loads(
    requests.get(
        base_url+"audio-features/21YxK0klhpfLW8budkJaMF", 
        headers=headers, params=params).content)


if response:
    print (response)
else:
    print(f"Error {response.status_code}")
    print(response.content)