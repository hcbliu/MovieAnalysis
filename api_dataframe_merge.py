
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

# For caching part 1 of the dataframe, looping over the movieDF dataframe from row 0 to 7500
for line in movieDF.index[:7500]:
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
cleandMovieDF.to_csv('cleanedMovieDataPart1.csv')


# For caching part 2 of the dataframe, looping over the movieDF dataframe from row 7500 to 14000
for line in movieDF.index[7500:14000]:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
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
cleandMovieDF.to_csv('cleanedMovieDataPart2.csv')


# For caching part 3 of the dataframe, looping over the movieDF dataframe from row 15000 to 19000 (skipping [14000:15000])
for line in movieDF.index[15000:19000]:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
        pass
    elif line == 18752: 
        pass
    elif line == 18826: 
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
cleandMovieDF.to_csv('cleanedMovieDataPart3.csv')


# For caching part 4 of the dataframe, looping over the movieDF dataframe from row 21000 to 22750 (skipping [19000:21000])
for line in movieDF.index[21000:22750]:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
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
cleandMovieDF.to_csv('cleanedMovieDataPart4.csv')


# For caching part 5 of the dataframe, looping over the movieDF dataframe from row 23000 to 25500 (skipping [22750:23000])
for line in movieDF.index[23000:25500]:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
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
cleandMovieDF.to_csv('cleanedMovieDataPart5.csv')


# For caching part 6 of the dataframe, looping over the movieDF dataframe from row 26000 to 27300 (skipping [25500:26000])
for line in movieDF.index[26000:27300]:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
        pass
    elif line == 26603: 
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
cleandMovieDF.to_csv('cleanedMovieDataPart6.csv')


# For caching part 7 of the dataframe, looping over the movieDF dataframe from row 27400 to the end (skipping [27300:22400])
for line in movieDF.index[27400:]:
    movieYear = movieDF['year'].iloc[line] 
    movieTitle = movieDF['title'].iloc[line]
    apiMatch = fetchMovie(movieTitle)
    if apiMatch.empty == True:
        pass
    elif movieTitle == 'Missing': 
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
cleandMovieDF.to_csv('cleanedMovieDataPart7.csv')

# for line in movieDF.index:
#     movieYear = movieDF['year'].iloc[line] 
#     movieTitle = movieDF['title'].iloc[line]
#     apiMatch = fetchMovie(movieTitle)
#     if apiMatch.empty == True:
#         pass
#     elif movieTitle == 'Missing': 
#         pass
#     elif line == 4141: 
#         pass
#     elif line == 4185: 
#         pass
#     elif line == 5760: 
#         pass
#     elif line == 7670: 
#         pass
#     elif line == 8180: 
#         pass
#     elif line == 9157: 
#         pass
#     elif line == 10107: 
#         pass
#     elif line == 11794: 
#         pass
#     elif line == 13798: 
#         pass
#     elif line == 18752: 
#         pass
#     elif line == 18826: 
#         pass
#     elif line == 19058: 
#         pass
#     elif line == 20860: 
#         pass    
#     elif line == 21047: 
#         pass
#     elif line == 21062: 
#         pass
#     elif line == 21181: 
#         pass
#     elif line == 21479: 
#         pass
#     elif line == 21539: 
#         pass
#     elif line == 21584: 
#         pass
#     elif line == 22570: 
#         pass
#     elif line == 23151: 
#         pass
#     elif line == 23443: 
#         pass
#     elif line == 23452: 
#         pass
#     elif line == 24075: 
#         pass
#     elif line == 24976: 
#         pass
#     elif line == 26603: 
#         pass
#     elif line == 28767: 
#         pass   
#     elif line == 28877: 
#         pass   
#     elif line == 29278: 
#         pass
#     elif line == 29522: 
#         pass            
#     elif type(apiMatch['Release Date'].values[0]) == float: 
#         pass
#     else:
#         try: 
#             x = int(apiMatch['Release Date'].values[0])
#         except ValueError: 
#             pass
#         if re.search(r'[^0123456789]', apiMatch['Release Date'].values[0]) ==None:
#             ValueError
#             pass 
#         if apiMatch['Release Date'].values[0][:4] == str: 
#             print(line)
#             pass
#         apiYear = int(apiMatch['Release Date'].values[0][:4])
#         if apiMatch['Release Date'].empty == True:
#             pass 
#         elif apiYear == movieYear: 
#             movieDF['synopsis'].iloc[line] = apiMatch['Synopsis'].values[0]

# cleandMovieDF = movieDF[movieDF['synopsis'].notna()]

# # When I ran this part of the code, I changed the 'partN' part to 'part1', 'part2', 'part3', etc. to generate 7 different files.
# cleandMovieDF.to_csv('cleanedMovieDataAPIpartN.csv')

   
