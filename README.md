# Movie Analysis
This project is currently in progress. The goal is to evaluate movies by criteria relating to gender.

## Objective  
Our goal is to create an app that displays information about movies. For example, a user may want to know how socially conscious the movie Inception is. The app prompts the user to type in the name of the movie, and then returns information about the movie which includes: movie title, release year, short synopsis, Bechdel test scores, explanation of the test scores, % of cast that are women.

## Structure  
The respository is structured as follows:

DOCUMENTS:
-Readme (this doc): summarizes most important information about the project
-docs folder: this contains important info about the project (essentially a subset of our shared google drive)

CODE AND CSVs:
-mastercode.py: this initial code combines the Kaggle and scraping work. It generates movietests_20200227_v2.csv.
-api_dataframe_merge.py: adds synopsis data from the API. It outputs all of the CSV files starting cleanedMovieData and ending with numbers.
-merge_cleaned_movieDF.py: Merges the 7 files starting with cleanedMovieData and creates cleanedMovieDataFinal.csv.
-menu_final.py: This lets users see information from cleanedMovieDataFinal.csv.

 
Everyone also has an individual branch containing the original work that they sent via email as of 2.26.20.

## Data  
Data sources are listed below:  
CSV files: https://www.kaggle.com/rounakbanik/the-movies-dataset  
Web scraping: https://bechdeltest.com/  
API work: https://developers.themoviedb.org/3/getting-started/introduction  
Note: since the CSV files were too large to be uploaded to GitHub, they are saved on Gootle Drive here: https://drive.google.com/drive/folders/1YBz5KyT-jH_OTG0yfxhmN35hdNdsBP5V?usp=sharing.

