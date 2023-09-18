from spoty_parser import SpotyParser
querier = SpotyParser()
print(querier.query('top n artists', 10))