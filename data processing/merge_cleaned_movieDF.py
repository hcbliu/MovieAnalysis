import pandas as pd

movieDF1 = pd.read_csv('cleanedMovieDataPart1.csv')
movieDF2 = pd.read_csv('cleanedMovieDataPart2.csv')
movieDF3 = pd.read_csv('cleanedMovieDataPart3.csv')
movieDF4 = pd.read_csv('cleanedMovieDataPart4.csv')
movieDF5 = pd.read_csv('cleanedMovieDataPart5.csv')
movieDF6 = pd.read_csv('cleanedMovieDataPart6.csv')
movieDF7 = pd.read_csv('cleanedMovieDataPart7.csv')


bigmovieDF = movieDF1.copy()
bigmovieDF = bigmovieDF.append(movieDF2, ignore_index=True)
bigmovieDF = bigmovieDF.append(movieDF3, ignore_index=True)
bigmovieDF = bigmovieDF.append(movieDF4, ignore_index=True)
bigmovieDF = bigmovieDF.append(movieDF5, ignore_index=True)
bigmovieDF = bigmovieDF.append(movieDF6, ignore_index=True)

bigmovieDF.to_csv('cleanedMovieDataFINAL.csv')