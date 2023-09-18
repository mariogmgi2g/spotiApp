from spoty_parser import SpotyParser
import json
import pandas as pd

id_playlist = '37i9dQZF1DWWGFQLoP9qlv'
querier = SpotyParser()

respuesta1 = querier.query('top n artists', 10)
respuesta2 = list(querier.query('top n genres', 10))
respuesta3 = querier.query('top n tracks', 10)
respuesta4 = querier.query('top n tracks artists', 10)
respuesta5 = list(querier.query('playlist tracks', id_playlist).keys())
respuesta6 = querier.query('track features from playlist', id_playlist)

data = {
    'top 10 artists': respuesta1,
    'top genres': respuesta2, 
    'top 10 tracks': respuesta3, 
    'top tracks artists': respuesta4, 
    'playlist tracks ' + id_playlist: respuesta5, 
    'track features from playlist': respuesta6, 
}
print(data)
with open('./data.json', 'w') as fp:
    json.dump(data, fp)



