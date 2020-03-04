
import json
import requests
import pandas as pd
import numpy as np
import re

movieDF = pd.read_csv('movietests_20200227_v2.csv')
movieDF['synopsis'] = np.nan


def fetchMovie(movie):
    headers = {'Content-Type': 'application/json'}
    url = 'https://api.themoviedb.org/3/search/movie?api_key=b968f575fb5dee1efeea8edc5e6198a3&query=' + str(movie)
    response = requests.get(url, headers = headers)
    if response.status_code != 200:
        raise RuntimeError('API failed')
    data = json.loads(response.content.decode('utf-8'))
    if data['results'] == []: 
        return pd.DataFrame()
    else: 
        df = pd.io.json.json_normalize(data['results'])
        df.rename(columns={"title" : "Title", "release_date" : "Release Date", "overview" : "Synopsis"}, inplace=True)
        return df[['Title', 'Release Date', 'Synopsis']]

#I ran into an API Runtime error while looping over the entire dataframe (around 30,000 rows). Pass bypass the issue, I got a second API key and ran this code in chunks.
# By chunking I mean changing line 29 of the code (for line in movieDF.index:) to (for line in movieDF.index[:7500]:), (for line in movieDF.index[7500:15000]:), (for line in movieDF.index[1500:2250]:)

for line in movieDF.index:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
        pass
    elif line == 4141: 
        pass
    elif line == 4185: 
        pass
    elif line == 5760: 
        pass
    elif line == 7670: 
        pass
    elif line == 8180: 
        pass
    elif line == 9157: 
        pass
    elif line == 10107: 
        pass
    elif line == 11794: 
        pass
    elif line == 13798: 
        pass
    elif line == 18752: 
        pass
    elif line == 18826: 
        pass
    elif line == 19058: 
        pass
    elif line == 20860: 
        pass    
    elif line == 21047: 
        pass
    elif line == 21062: 
        pass
    elif line == 21181: 
        pass
    elif line == 21479: 
        pass
    elif line == 21539: 
        pass
    elif line == 21584: 
        pass
    elif line == 22570: 
        pass
    elif line == 23151: 
        pass
    elif line == 23443: 
        pass
    elif line == 23452: 
        pass
    elif line == 24075: 
        pass
    elif line == 24976: 
        pass
    elif line == 26603: 
        pass
    elif line == 28767: 
        pass   
    elif line == 28877: 
        pass   
    elif line == 29278: 
        pass
    elif line == 29522: 
        pass            
    elif type(apiMatch['Release Date'].values[0]) == float: 
        pass
    else:
        try: 
            x = int(apiMatch['Release Date'].values[0])
        except ValueError: 
            pass
        if re.search(r'[^0123456789]', apiMatch['Release Date'].values[0]) ==None:
            ValueError
            pass 
        if apiMatch['Release Date'].values[0][:4] == str: 
            print(line)
            pass
        apiYear = int(apiMatch['Release Date'].values[0][:4])
        if apiMatch['Release Date'].empty == True:
            pass 
        elif apiYear == movieYear: 
            movieDF['synopsis'].iloc[line] = apiMatch['Synopsis'].values[0]

cleandMovieDF = movieDF[movieDF['synopsis'].notna()]

# When I ran this part of the code, I changed the 'partN' part to 'part1', 'part2', 'part3', etc. to generate 7 different files.
cleandMovieDF.to_csv('cleanedMovieDataAPIpartN.csv')

   
