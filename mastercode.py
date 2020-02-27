##################
# Movie Analysis #
##################
#Authors: Sinduja Sriskanda, Hui-Chen Betty Liu, Kamaneeya Kalaga, Kayla Reiman

#Note: As of 2.27.20, this file contains code by Sindu, Kayla, and Kamaneeya. 
#The end product is a dataframe with movie titles, years, and results of 3 tests:
    # %women cast
    # %women crew
    # Bechdel test
#Note: Betty's API work has not yet been merged in.
#The final dataset at this point is ccurrently alled movietests_widedf_v2. 
#Although this name is a bit long, the thinking is as follows:
    #movietests means that it's integrating all tests
    #wide indicates that it's on the movie level (instead of movie/person)
    #df indicates it's a pandas dataframe
    #v2 indicates it's had some cleaning
    
####################
# Import Libraries #
####################
import pandas as pd
from bs4 import BeautifulSoup
import requests

#################################
# Read Movie Datasets from CSVs #
#################################

#Challenge: datasets are too large to save on GitHub, so individuals using this 
#code must first download to their local drives. The data are from kaggle:
#https://www.kaggle.com/rounakbanik/the-movies-dataset

#The relevant files are also saved here for convenience:
#https://drive.google.com/drive/folders/1YBz5KyT-jH_OTG0yfxhmN35hdNdsBP5V?usp=sharing

#After setting directory, import appropiate csv files into data frames
moviemetadata = pd.read_csv('movies_metadata.csv', engine = 'python')
moviecredits = pd.read_csv('credits.csv', engine = 'python')

#Define a function to view the datasets
#Input: dsname = dataframe
#Returned: nothing -- this is just for printing
def viewdata(dsname, desc = 'add description here'):
    name =[x for x in globals() if globals()[x] is dsname][0]
    print('------------------------------------------------------')
    print('THREE-PART OVERVIEW OF', name.upper())
    print('Description:', desc)
    print('  1. Columns in', name)
    for i in range(len(dsname.columns)):
        print('\t', dsname.columns[i], end ='\n')
    print('  2. Shape of dataframe:', dsname.shape)
    print('\n  3. Use head() to see 5 Rows')
    print(dsname.head()) 
    
viewdata(moviemetadata, 'This is an original CSV from kaggle.')
viewdata(moviecredits, 'This is an original CSV from kaggle.')

#######################
# Sindu work on CSVs  #
#######################
'''
Author: Sinduja Sriskanda
Date:  02/26/20

Purpose:
The cast and crew columns were not not in an easily
usable format, so Sindu processed the CSVs to create two dataframes:
   1) castdf shows which cast members are in each movie (each row has a movie/person combination)
   2) crewdf shows which crew members are in each movie (also movie/person level)
worked on each movie. Ultimately, in spite of all of the work to translate
the entries to JSON form so that they could be loaded, some of the
entries were unreadable.
'''

#PART 1: CREATION OF DATAFRAME FOR CAST
#Isolating the cast column and id columns
cast = moviecredits[['cast', 'id']]

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

#KR addition: view the dataset
viewdata(castdf, 'This is half of the processed form of moviecredits from Kaggle.')

#PART 2: CREATION OF DATAFRAME FOR CREW
#(it's basically the same stuff I was doing before)
#I decided to add information on Department and Job in case we want to look into those

crew = moviecredits[['crew', 'id']]

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

#KR addition: view the dataset
viewdata(crewdf, 'This is half of the processed form of moviecredits from Kaggle.')

##############################
# Kamaneeya work on scraping #
##############################
#### BECHDEL TEST WORK #####
'''
Author:  Kamaneeya Kalaga
Date:  02/21/2020

Purpose:
This code scrapes the data of movie title, its bechdel test score (0-3)
and the description of the score for each year and creates a pandas dataframe
with the information.
'''

# Years of data needed --> can be edited
#KR updated to include whole range rather than just being most recent 3 years. 
#Next step is figure out which years are actually on the website, in order to be efficient.
years = [str(x) for x in list(range(1980, 2020))]

# Create Empty dataset to fill the data
bechdel_test = pd.DataFrame(columns = ["year", "title", "score", "description"])

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
        bechdel_test = bechdel_test.append({"year":yr, "title":name, "score": score[2], "description": desc[1:-1]}
                ,ignore_index = True)

#Set up titles that will have no differences in spaacing or capitalization
#KR addition: view the dataset
viewdata(bechdel_test, 'This web-scrabed dataframe shows how movies fared on the Bechdel test.')

#######################
# Kayla work on merge #
#######################
'''
Author: Kayla Reiman
Date:  02/27/20

The goal is to create a dataset of movie titles, which can be queried 
for information on 3 main outcomes:
    -% women in the cast
    -% women in the crew
    -% Bechdel test information

Steps include the following:
    1. Collapse Sindu's movie/person-level datasets into movie-level data
    2. Create a dataset with movies' titles/years
    3. Merge cast, crew, and title information on the movie level
    4. Merge Sindu and Kamaneeya's work into a single dataset based on title/year
    5. Clean the data (incomplete)
    
'''

##### STEP 1.COLLAPSE SINDU'S WORK TO MOVIE-LEVEL ####

#Remove rows w/ missing gender data b/c we don't have a way of replacing it
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

#Check that woman and gender line up correctly by looking at a few observations
castdf.head(15)
crewdf.head(20)

#Goal: Create 4 dataframes, which collapse movie/person-level data to the person-level
#Additional notes: 
#I have noticed that some movies have small samples, and it will be misleading
#if a movie only has 1 person in the crew list who is a man to say that 
#the movie has 0% women. Therefore, I am also creating series
#that show the sample size for each movie.
#In SQL, I know how to do all this in a single step using groupby/merge/case_when,
#but in Python this piecemeal method is currently my best work. Input
#on more efficient methods would be welcome.
castwide = pd.DataFrame(castdf.groupby('id')["woman"].mean()) #% women in cast
crewwide = pd.DataFrame(crewdf.groupby('id')["woman"].mean())
castnum = pd.DataFrame(castdf.groupby('id').size()) # number of people in cast data
crewnum = pd.DataFrame(crewdf.groupby('id').size())

#####2. STEP 2: READ TITLES ####
#Create a series just for titles/dates and make it work like the other dataframes
#Since the index here was a string, I updated Sindu's work to also have the ID field be strings

#Read in version 1 of the titles, including titles, IDs, and release date
titlesv1 = pd.DataFrame( {'title': moviemetadata["original_title"], \
                          'id':moviemetadata["id"], 'date':moviemetadata["release_date"]})
    
#Change the id field from a column to an index
titlesv2 = titlesv1.set_index('id')

#Fill date field so that next operation (creating a year variable) works
titlesv3 = titlesv2.fillna('0000')

#Create a year field
titlesv3["year"] = titlesv3.date.apply(lambda x: x[:4])

#Remove the release date field to keep the dataset limited to only relevant info
titlesv4 = titlesv3[["title", "year"]]

#Check that everything worked correctly
viewdata(titlesv4, 'This is the processed version of the moviemetadata from kaggle.')
        
#####3. STEP 3: MERGE SINDU'S DATAFRAMES #######
#Merge all columns on cast/crew gender using the id field. Note that these datasets
#all have the same ID field because they are from here:
#https://www.kaggle.com/rounakbanik/the-movies-dataset.
#Note: These are outer joins b/c I want to keep all these titles, whether or not
#they have cast/crew data available.
castcrew_widedf = titlesv4.merge(crewwide,on='id',how ='outer').\
merge(crewnum,on = 'id',how ='outer').\
merge(castwide,on='id',how ='outer').\
merge(castnum,on='id',how ='outer')

#Re-name the columns after processing. Note: I am using all lower case for consistency
castcrew_widedf.columns = ['title', 'year', 'crew_pct_women', 'crew_n', \
                           'cast_pct_women', 'cast_n']

print('View the new wide dataset')
viewdata(castcrew_widedf, 'This is the the merge of all Kaggle datasets on the movie level')

##### STEP 4: MERGE SINDU'S WORK W/ KAMANEEYA'S WORK #######
##### CRUCIAL NOTE: THIS CURRENTLY USES A RIGHT JOIN, INSTEAD OF AN OUTER #####
#Creating a merge key that uses all caps and concatenates years and titles w/o spaces.
#The goals here are two-fold:
#1) by making everything upper-case without spaces, this minimizes the probability
#That the same movie could be expressed slightly differently across databases
#2) by adding the year, this separates remakes (eg. Freaky Friday, Little Women...)
castcrew_widedf["mergekey"] = castcrew_widedf['title'].apply(lambda x: x.upper()).\
apply(lambda y: y.replace(' ', '')) + castcrew_widedf.year
bechdel_test["mergekey"] = bechdel_test['title'].apply(lambda x: x.upper()).\
apply(lambda y: y.replace(' ', ''))+ bechdel_test.year

#Merge the gender fields above (in castcrew_widedf) with the titles and bechdel datasets
#Note: for now using right join so that can see how Bechdel matches.
#However, should ultimately use outer join.
movietests_widedf_v1 = pd.merge(castcrew_widedf, bechdel_test, how = 'right', on = 'mergekey')

print('View the new fully merged dataset')
viewdata(movietests_widedf_v1, 'This merges Kaggle and web-scraped data.')


#### QUALITY CHECKS ON MERGES
#KR notes on next steps:
#Ideally use 20 randomly select obs, rather than using head()
#Run further checks on partial duplicates to check 
    #a) which data are accurate (particularly in Beneath)
    #b) which obs should we delete?
#Confirm the current warning isn't causing problems:
    #"UserWarning: Boolean Series key will be reindexed to match DataFrame index."

print('QUALITY CHECK: Print 20 obs where the titles do not match:\nNote: looks like capitalization diffs:')
print(movietests_widedf_v1[movietests_widedf_v1.title_x != movietests_widedf_v1.title_y]\
                           [pd.notnull(movietests_widedf_v1.title_x)]\
                           [pd.notnull(movietests_widedf_v1.title_y)][['title_x', 'title_y']].head(20))

print('QUALITY CHECK: Print 20 obs the years do not match:')
print('Note: this lack of issues makes sense b/c years do not have capitalization diffs')
print(movietests_widedf_v1[movietests_widedf_v1.year_x != movietests_widedf_v1.year_y]\
                           [pd.notnull(movietests_widedf_v1.year_x)]\
                           [pd.notnull(movietests_widedf_v1.year_y)][['year_x', 'year_y']].head(20))

#Note: I would like to improve the check below for efficiency, but this shows at least that
#there's some variation across movies.
print('''QUALITY CHECK: Print 20 obs to check if movies where titles did not match up correctly still have
some data from both CSV sources (ex. cast_pct_women) and Bechdel (ex. score)
Note: This looks positive b/c all have Bechdel results, but this makes sense b/c right-join.''')
print(movietests_widedf_v1[movietests_widedf_v1.title_x != movietests_widedf_v1.title_y]\
                           [pd.notnull(movietests_widedf_v1.title_x)]\
                           [pd.notnull(movietests_widedf_v1.title_y)]\
                           [['title_x', 'cast_pct_women', 'score']].head(20))

print('''DUPLICATE CHECK ON THE TITLE LEVEL:
      Print 20 observations w/ duplicate titles to see whether they have both CSV and Bechdel data.
      Note: Looks like there are some data issues in movies (eg. Beneath), but others
      are just different versions of the movie over time (eg. Annie).''')
t_dups = movietests_widedf_v1.groupby('title_x') # number of people in cast data
t_dups.filter(lambda x: len(x) > 1).sort_values(by = 'title_x')[['title_x','year_x', 'cast_pct_women', 'score']].head(20)

print('''DUPLICATE CHECK ON THE TITLE/YEAR LEVEL: 
         Add year to the group_by and look at whether the data match across title/year duplicates.
         Note: This is concerning because a few entries (Beneath, Emma) have differnet 
         cast_pct_women values across the two entries.''')
ty_dups = movietests_widedf_v1.groupby(['title_x', 'year_x']) # number of people in cast data
ty_dups.filter(lambda x: len(x) > 1).sort_values(by = 'title_x')[['title_x','year_x', 'cast_pct_women', 'score']].head(20)

#### STEP 5: DATA CLEANING ####
#KR note as of 2.27.20: This is just a start to data cleaning. Next steps include the following:
    #Check that missing values were replaced correctly
    #Learn to write code for "insufficient sample" w/o getting the SettingWithCopyWarning
#Rename versions of title/year we want to keep
movietests_widedf_v1.rename({'title_x' : 'title', 'year_x':'year'}, axis = 1, inplace = True)
###NEXT DATA CLEANING STEP TO ADD HERE: Remove duplicate probs found in the quality checks above.

#Drop extra vars from merge
movietests_widedf_v2 = movietests_widedf_v1.drop(['mergekey', 'title_y','year_y'], axis=1)

#Address the insufficient sample on certain movies
movietests_widedf_v2['cast_pct_women'][movietests_widedf_v2['cast_n'] <= 10] \
= 'insufficient sample'
movietests_widedf_v2['crew_pct_women'][movietests_widedf_v2['crew_n'] <= 10] \
= 'insufficient sample'
movietests_widedf_v2.fillna('Missing', inplace = True)

print('Check that missing values have been replaced by printing 20 obs from the kaggle data')
print(movietests_widedf_v2[['crew_pct_women', 'cast_pct_women']].head(20))

viewdata(movietests_widedf_v2, 'This contains some cleaning after the final merge. It is currently the final dataset.')


#### EXPLORATION OF FULL OUTER JOIN #####
print('------------------------------------------------------------------------------')

#RE-MERGE SINDU'S AND KAMANEEYA'S WORK USING AN OUTER JOIN. This will include all of Sindu's 
#records, even when they do not have Bechdel data.
movietests_outer_v1 = pd.merge(castcrew_widedf, bechdel_test, how = 'outer', on = 'mergekey')
print('OUTER JOIN View how the dataset looks with an OUTER join')
viewdata(movietests_outer_v1, 'This merges Kaggle and web-scraped data.')

print('OUTER JOIN QUALITY CHECK: Print 20 obs where the titles do not match')
print(movietests_outer_v1[movietests_outer_v1.title_x != movietests_outer_v1.title_y]\
                           [pd.notnull(movietests_outer_v1.title_x)]\
                           [pd.notnull(movietests_outer_v1.title_y)][['title_x', 'title_y']].head(20))

print('OUTER JOIN QUALITY CHECK: Print 20 obs the years do not match:')
print(movietests_outer_v1[movietests_outer_v1.year_x != movietests_outer_v1.year_y]\
                           [pd.notnull(movietests_outer_v1.year_x)]\
                           [pd.notnull(movietests_outer_v1.year_y)][['year_x', 'year_y']].head(20))

#Note: I would like to improve the check below for efficiency, but this shows at least that
#there's some variation across movies.
print('''OUTER JOIN QUALITY CHECK: Print 20 obs to check if movies where titles did not match up correctly still have
some data from both CSV sources (ex. cast_pct_women) and Bechdel (ex. score)
Note: This should depart from the right-join above.''')
print(movietests_outer_v1[movietests_outer_v1.title_x != movietests_outer_v1.title_y]\
                           [pd.notnull(movietests_outer_v1.title_x)]\
                           [pd.notnull(movietests_outer_v1.title_y)]\
                           [['title_x', 'cast_pct_women', 'score']].head(20))

print('OUTER JOIN DUPLICATE CHECK ON THE TITLE LEVEL:')
t_dups2 = movietests_outer_v1.groupby('title_x') # number of people in cast data
t_dups2.filter(lambda x: len(x) > 1).sort_values(by = 'title_x')[['title_x','year_x', 'cast_pct_women', 'score']].head(20)

print('OUTER JOIN DUPLICATE CHECK ON THE TITLE/YEAR LEVEL')
ty_dups2 = movietests_outer_v1.groupby(['title_x', 'year_x']) # number of people in cast data
ty_dups2.filter(lambda x: len(x) > 1).sort_values(by = 'title_x')[['title_x','year_x', 'cast_pct_women', 'score']].head(20)

#### STEP 5: DATA CLEANING ####
#KR note as of 2.27.20: This is just a start to data cleaning. Next steps include the following:
    #Check that missing values were replaced correctly
    #Learn to write code for "insufficient sample" w/o getting the SettingWithCopyWarning
#Rename versions of title/year we want to keep
movietests_outer_v1.rename({'title_x' : 'title', 'year_x':'year'}, axis = 1, inplace = True)
###NEXT DATA CLEANING STEP TO ADD HERE: Remove duplicate probs found in the quality checks above.

#Drop extra vars from merge
movietests_outer_v1 = movietests_outer_v1.drop(['mergekey', 'title_y','year_y'], axis=1)

#Address the insufficient sample on certain movies
movietests_outer_v1['cast_pct_women'][movietests_outer_v1['cast_n'] <= 10] \
= 'insufficient sample'
movietests_outer_v1['crew_pct_women'][movietests_outer_v1['crew_n'] <= 10] \
= 'insufficient sample'
movietests_outer_v1.fillna('Missing', inplace = True)

print('Check that missing values have been replaced by printing 20 obs from the kaggle data')
print(movietests_outer_v1[['crew_pct_women', 'cast_pct_women']].head(20))

viewdata(movietests_outer_v1, 'This contains some cleaning after the final OUTER JOIN merge.')
