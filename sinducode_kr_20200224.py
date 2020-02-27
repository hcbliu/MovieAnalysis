#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 12:55:07 2020

@author: ssriskanda
"""

#importing libary
import pandas as pd

#importing appropiate csv files into data frame
#KR note: Just edited paths to work on my computer
OscarDemographics = pd.read_csv('Oscars-demographics-DFE.csv', engine = 'python')
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
    iden = metacast[i][1]
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
castdf.columns = ['Names', 'Movie ID', 'Gender']


for i in range(len(castdf)):
    if castdf.iloc[i]['Movie ID'] in Oscarmetadata.iloc[i]['id']:
        castdf.replace(to_replace = castdf.iloc['Movie ID'][i], value = Oscarmetadata.iloc['id'][i] )
    else:
        continue
    
            

#To merge with demographics, 
#we first need to edit out those who won "Best Director" since those aren't
#exactly actresses (unless we would want to keep that if there is a test for that?)

#KR note: I think the demographics dataset is just too small to be useful :( :( :(


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
    iden = metacrew[i][1]
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
    for dic in finalcrew[i][0]:
        try:
            iden = dic['id']
            name = dic['name']
            department = dic['department']
            job = dic['job']
            gender = dic['gender']
        except TypeError:
            continue
        else:
            pdfinalcrew.append([name, iden, department, job, gender])
crewdf = pd.DataFrame(pdfinalcrew)
crewdf.columns = ['Names', 'ID', 'Department', 'Job', 'Gender']        

#Part 3: DESCRIPTIVE ANSLYSIS
        
        

    
    





