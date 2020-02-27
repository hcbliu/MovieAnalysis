#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:55:07 2020

@author: ssriskanda
"""

#importing libary
import pandas as pd

#importing appropiate csv files into data frame
OscarPicInfo = pd.read_csv('pictures.csv', engine = 'python')
Oscarmetadata = pd.read_csv('movies_metadata.csv', engine = 'python')
Oscarcredits = pd.read_csv('credits.csv', engine = 'python')

#PART 1: CREATION OF DATAFRAME FOR CAST

#Since I am only trying to manipulate the cast columns, I decided to isolate it
#in case I make any mistakes
#KR note: I think we need to keep the id column from the Oscarcredits dataframe
#so that it can ultimately be merged with metadata to extract the title and year.
#That said, I couldn't figure out how to preserve your work below without limiting
#to just cast. So...this is a mystery!
cast = Oscarcredits[['cast', 'id']]

#As mentioned before, I didn't know if the dataframe was 
#stopping me from manipulating the data, so I decided to append it into a list
#this was when I realized that they were strings...not dictionaries

metacast = []
for string in cast.index:
    entry = [cast['cast'][string], cast['id'][string]]
    metacast.append(entry)
    

#All of these metacast lists is just different manipulation of the same data
#to make it a friendlier format. This is just another "meta list" to remove 
#characters and make it a dictionary format so it can be converted later on
#The fact that the string has the list [] is making it difficult to convert so 
#I removed those and made ' to "
#**Also had to make a new list since I tried to change it with metacast and nothing was
#changing.. it's a little clunky but it works sooooooo ya
    
metacast2 = []
for i in range(len(metacast)):
    name = metacast[i][0]
    iden = metacast[i][1].astype(str)
    name = name.replace("'", '"')
    name = name.replace("[", "")
    name = name.replace("]", "")
    metacast2.append([name, iden])
        

#the final cast list is the list of dictionaries this should be producting
#used eval() function since JSON wasn't working for me. Managed to recover
#29288 flims (out of 45476 films) 

finalcast = []
for i in range(len(metacast2)):
    string = metacast2[i][0]
    iden = metacast2[i][1]
    try:
        convert = eval(string)
    except SyntaxError:
        continue
    else:
        finalcast.append([convert,iden])

#Created dataframe of all the actors who have won
#I have been bumping into issues where this would not iterate through all of the dictionaries
#So I put a try-block and just skip those that are not working
#If you can find a way to maybe??? 
#KR note: Added in gender.    
        
pdfinalcast = []
for i in range(len(finalcast)):
    iden = finalcast[i][1]
    for dic in finalcast[i][0]:
        try:
            name = dic['name']
            gender = dic['gender']
        except TypeError:
            continue
        else:
            pdfinalcast.append([name, iden, gender])
castdf = pd.DataFrame(pdfinalcast)
castdf.columns = ['name', 'id', 'gender']


#PART 2: CREATION OF DATAFRAME FOR CREW
#(it's basically the same stuff I was doing before)
#I decided to add information on Department and Job in case we want to look into those

        
crew = Oscarcredits[['crew', 'id']]      
        
metacrew = []
for string in crew.index:
    entry = [crew['crew'][string], crew['id'][string]]
    metacrew.append(entry)
    
metacrew2 = []
for i in range(len(metacrew)):
    name = metacrew[i][0]
    iden = metacrew[i][1].astype(str)
    name = name.replace("'", '"')
    name = name.replace("[", "")
    name = name.replace("]", "")
    metacrew2.append([name, iden])
               
 
finalcrew = []
for i in range(len(metacrew2)):
    string = metacrew2[i][0]
    iden = metacrew2[i][1]
    try:
        convert = eval(string)
    except SyntaxError:
        continue
    else:
        finalcrew.append([convert,iden])       
        
pdfinalcrew = []
for i in range(len(finalcrew)):
    iden = finalcrew[i][1]
    for dic in finalcrew[i][0]:
        try:
            name = dic['name']
            department = dic['department']
            job = dic['job']
            gender = dic['gender']
        except TypeError:
            continue
        else:
            pdfinalcrew.append([name, iden, department, job, gender])
crewdf = pd.DataFrame(pdfinalcrew)
crewdf.columns = ['name', 'id', 'department', 'job', 'gender'] 

#Part 3: Collapse data to the movie level (aka transform from long to wide)

        
#Remove rows w/ missing data
castdf = castdf[castdf['gender'] != 0]
crewdf = crewdf[crewdf['gender'] != 0]


#Create new gender field that's a binary for whether somebody is a woman
def newgender(gender):
    if gender == 2:
        woman = 0
    elif gender == 1:
        woman = 1
    elif gender == 0:
        woman = 'NaN'
    return woman
        
castdf['woman'] = castdf['gender'].apply(newgender)
crewdf['woman'] = crewdf['gender'].apply(newgender)

#Check that woman and gender line up correctly by looking at a few obs
castdf.head(15)
crewdf.head(15)

#Create 4 different series that will ultimately comprise our dataset
castwide = pd.DataFrame(castdf.groupby('id')["woman"].mean()) #% women in cast
crewwide = pd.DataFrame(crewdf.groupby('id')["woman"].mean())
castnum = pd.DataFrame(castdf.groupby('id').size()) # number of people in cast
crewnum = pd.DataFrame(crewdf.groupby('id').size())

######TITLES########
#Create a series just for titles and make it work like the other dataframes
titlesv1 = pd.DataFrame( {'title': Oscarmetadata["original_title"], \
                          'id':Oscarmetadata["id"], 'date':Oscarmetadata["release_date"]})
titlesv2 = titlesv1.set_index('id')
titlesv3 = titlesv2.fillna('0000')
titlesv3["year"] = titlesv3.date.apply(lambda x: x[:4])
titlesv4 = titlesv3[["title", "year"]]
titlesv4.head()

##### MERGE #######
#Merge all 4 columns + titles
wide_v1 = titlesv4.merge(crewwide,on='id',how ='outer').\
merge(crewnum,on = 'id',how ='outer').\
merge(castwide,on='id',how ='outer').\
merge(castnum,on='id',how ='outer')

wide_v1.columns = ['title', 'year', 'crew_women', 'crew_ppl', 'cast_women', 'cast_ppl']
wide_v1.head()

#### BECHDEL TEST WORK #####
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
years = ['2021', '2020', '2019', '2018', '2017', '2016', \
         '2015', '2014', '2013', '2012', '2011']

# Create Empty dataset to fill the data
bechdel_test = pd.DataFrame(columns = ["Year", "Title", "Score", "Description"])

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
        bechdel_test = bechdel_test.append({"Year":yr, "title":name, "score": score[2], "description": desc[1:-1]}
                ,ignore_index = True)

#Set up titles that will have no differences in spaacing or capitalization
        
#Note: for now using right join so that can see how Bechdel matches
wide_v1["mergekey"] = wide_v1['title'].apply(lambda x: x.upper()).\
apply(lambda y: y.replace(' ', '')) + wide_v1.year
bechdel_test["mergekey"] = bechdel_test['title'].apply(lambda x: x.upper()).\
apply(lambda y: y.replace(' ', ''))+ bechdel_test.Year
multitest_v1 = pd.merge(wide_v1, bechdel_test, how = 'right', on = 'mergekey')

#### DATA CLEANING ####
#Address the insufficient sample on certain movies
multitest_v2 = multitest_v1.drop(['mergekey', 'title_x', 'Title', 'Score', 'Description', 'Year'], axis=1)  
multitest_v2['cast_women'][multitest_v2['cast_ppl'] <= 10] = 'insufficient sample'
multitest_v2['crew_women'][multitest_v2['crew_ppl'] <= 10] = 'insufficient sample'

multitest_v2.fillna('Missing')
