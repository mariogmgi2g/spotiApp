import requests
from auth import Auth
import json
import numpy as np
import pandas as pd
import random
import urllib.request

# Posibles instrucciones = 
#   -> top n artists
#   -> top n genres
#   -> top n tracks
#   -> top n tracks artists
#   -> track features
#   -> 

class SpotyParser:
    def __init__(self) -> None:
        self.__base_url = 'https://api.spotify.com/v1/'
        auth = Auth()
        token = auth.get_token()
        self.__headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }


    def query(self, query_key:str, *args) -> dict:
        implemented_query_keys = [
            'top n artists', 'top n genres', 'top n tracks', 
            'top n tracks artists', 'playlist cover image', 'playlist followers','playlist tracks', 'track features',
            'track features from playlist']

        if query_key == 'top n artists':
            (url_char, params) = SpotyParser.__query_top_artists(args[0], 0)
            response = self.__url_builder(url_char, params)
            response = SpotyParser.__get_top_artist(response)
        elif query_key == 'top n genres':
            (url_char, params) = SpotyParser.__query_top_artists(10, 0)
            response = self.__url_builder(url_char, params)
            response = SpotyParser.__get_top_m_genres(response, args[0])
        elif query_key == 'top n tracks':
            (url_char, params) = SpotyParser.__query_top_tracks(args[0], 0)
            response = self.__url_builder(url_char, params)
            response = SpotyParser.__get_top_tracks(response)
        elif query_key == 'top n tracks artists':
            (url_char, params) = SpotyParser.__query_top_tracks(args[0], 0)
            response = self.__url_builder(url_char, params)
            response = SpotyParser.__get_top_tracks_artists(response)

        elif query_key == 'playlist cover image':
            (url_char, params) = SpotyParser.__get_playlist_image(args[0])
            response = self.__url_builder(url_char, params)
            print(response)
            self.__download_playlist_image(response)

        elif query_key == 'playlist followers':
            (url_char, params) = SpotyParser.__get_playlist_followers(args[0])
            response = self.__url_builder(url_char, params)
            response = self.__followers(response)
            print(response)


        elif query_key == 'playlist tracks':
            (url_char, params) = SpotyParser.__query_playlist_tracks(args[0])
            response = self.__url_builder(url_char, params)
            response = SpotyParser.__get_playlist_tracks(response)
        elif query_key == 'track features':
            (url_char, params) = SpotyParser.__query_track_features(args[0])
            response = self.__url_builder(url_char, params)
            response = SpotyParser.__get_track_features(response)
        elif query_key == 'track features from playlist':
            playlist_id = args[0]
            # Se obtienen las canciones
            (url_char, params) = SpotyParser.__query_playlist_tracks(playlist_id)
            tracks_response = self.__url_builder(url_char, params)
            tracks = SpotyParser.__get_playlist_tracks(tracks_response)
            dict_response = {}
            # Se obtienen las características de las canciones
            for key in tracks.keys():
                (url_char, params) = SpotyParser.__query_track_features(tracks[key])
                response = self.__url_builder(url_char, params)
                response = SpotyParser.__get_track_features(response)
                dict_response[key] = response
        else: 
            raise ValueError(
                f"La instrucción no se encuentra entre aquellas implementadas, \
                las cuales son: {implemented_query_keys}")
        return response


    def __url_builder(self, url_char, params):
        response = json.loads(
            requests.get(
                self.__base_url + url_char, headers=self.__headers, params=params
            ).content
        )
        return response

    # --------------------------------------------------------------------------
    def __query_top_artists(n:int, offset:int=0) -> tuple:
        url_char = "me/top/artists"

        params = {
            'time_range' : 'medium_term',
            'limit' : n,
            'offset' : offset
        }
        return (url_char, params)


    def __get_top_artist(response:dict) -> list:
        top_artist = [response["items"][i]["name"] for i in range(len(response["items"]))]
        return top_artist


    def __get_top_m_genres(response:dict, n=5):
        no_flatten_list = [response["items"][i]["genres"] for i in range(len(response["items"]))]
        flatten_list = {}
        index = 0
        for i in no_flatten_list: 
            for j in i:
                flatten_list[index] = j
                index += 1
        return pd.Series(flatten_list).unique()[:5]
    
    # --------------------------------------------------------------------------
    def __query_top_tracks(n:int, offset:int=5) -> tuple:
        url_char = "me/top/tracks"

        params = {
            'time_range' : 'medium_term',
            'limit' : n,
            'offset' : offset
        }
        return (url_char, params)


    def __get_top_tracks(response:dict):
        top_tracks = [response["items"][i]["name"] for i in range(len(response["items"]))]
        return top_tracks
    

    def __get_top_tracks_artists(response):
        artists = [response["items"][i]["artists"] for i in range(len(response["items"]))]
        songs = [response["items"][i]["name"] for i in range(len(response["items"]))]
        dict_artists = dict(zip(songs, artists))
        for song in dict_artists.keys():
            list_artists = []
            for artist in dict_artists[song]:
                list_artists.append(artist["name"])
            dict_artists[song] = list_artists
        return dict_artists

    # --------------------------------------------------------------------------

    def __get_playlist_image(id_playlist:str):
        url_char = "playlists/" + id_playlist + "/images"
        params = {
            'time_range' : 'medium_term',
            'limit' : 10,
            'offset' : 0
        }
        return (url_char, params)

    def __download_playlist_image(self, response):
        image_url = response[0]['url']
        SpotyParser.download_image(image_url)

    def download_image(url):
        name = r'c:\Users\marin\OneDrive\Escritorio\CURSO_PHYTON\02_EPPY\act_02\spotiApp\cover'
        fullname = str(name)+".jpg"
        urllib.request.urlretrieve(url,fullname)
        


    def __query_playlist_tracks(id_playlist:str) -> tuple:
        #37i9dQZF1DWWGFQLoP9qlv
        url_char = "playlists/" + id_playlist

        params = {
            'time_range' : 'medium_term',
            'limit' : 10,
            'offset' : 0
        }
        return (url_char, params)
    
    def __get_playlist_followers(id_playlist:str):
        url_char = "playlists/" + id_playlist
        params = {
            'time_range' : 'medium_term',
            'limit' : 10,
            'offset' : 0
        }
        return (url_char, params)
    
    def __followers(self, response):
        response['followers']
        print(response)
    

    def __query_track_features(id_track:str) -> tuple:
        url_char = "audio-features/" + id_track

        params = {
            'time_range' : 'medium_term',
            'limit' : 10,
            'offset' : 0
        }
        return (url_char, params)
    

    def __get_playlist_tracks(response:dict):
        id_tracks = (response["tracks"]["items"][0])
        id_tracks = {response["tracks"]["items"][i]["track"]["name"]: response["tracks"]["items"][i]["track"]["href"].split("/")[-1] for i in range(len(response["tracks"]["items"]))}

        return id_tracks

    
    def __get_track_features(response) -> dict:
        features_of_interest = [
            'tempo', 'acousticness', 'danceability', 'energy', 
            'instrumentalness', 'liveness', 'loudness', 'valence']
        response2 = {
            key: response[key] 
            for key in response.keys() 
            if key in features_of_interest}
        return response2
    
    # --------------------------------------------------------------------------
    
