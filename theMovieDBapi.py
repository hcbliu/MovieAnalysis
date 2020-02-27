import json
import requests
import pandas as pd

movie = input('Enter movie name: ')

def fetchMovie(movie):
    headers = {'Content-Type': 'application/json'}
    url = 'https://api.themoviedb.org/3/search/movie?api_key=26ca1fcaf4653ea1e35333981c89e9e9&query=' + movie
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        raise RuntimeError('API failed')
    data = json.loads(response.content.decode('utf-8'))
    df = pd.io.json.json_normalize(data['results'])
    df.rename(columns={"title" : "Title", "release_date" : "Release Date", "overview" : "Overview"}, inplace=True)
    return df[['Title', 'Release Date', 'Overview']]

moviedf = fetchMovie(movie)
print(moviedf)



