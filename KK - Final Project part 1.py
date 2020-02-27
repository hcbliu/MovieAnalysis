'''
Author:  Kamaneeya Kalaga
Date:  02/21/2020

Purpose: 
This code scrapes the data of movie title, its bechdel test score (0-3) 
and the description of the score for each year and creates a pandas dataframe
with the information.

For now, the data will be have
 1 movie in 2021
 3 movies in 2020
 143 movies in 2019
'''

# Importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Years of data needed --> can be edited
years = ['2021', '2020', '2019']

# Create Empty dataset to fill the data
bechdel_test = pd.DataFrame(columns = ["Title", "Score", "Description"])

# Loop through each year to get the data
for yr in years:
    httpString ='http://bechdeltest.com/year/' + yr
    print(httpString)
    page = requests.get(httpString)
    
    # Scraping:
    # Parse the page
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Find the required tag
    movies = soup.find_all("div", class_ = "movie")
    
    for mov in movies:
        # Find the information
        info = mov.find_all("a")
        name = info[1].get_text()
        score = info[0].find("img")["alt"]
        desc = info[0].find("img")["title"]

        #Append to the dataframe
        bechdel_test = bechdel_test.append({"Title":name, "Score": score[2], "Description": desc[1:-1]}
                ,ignore_index = True)
    
print(bechdel_test)
