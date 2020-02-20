#This .py file is where we will create our final project.
#KR 2.20.20 -- this comment is an example of making changes within the github browser on the MASTER program.
##################
# Movie Analysis #
##################
#Authors: Sinduja Sriskanda, Hui-Chen Betty Liu, Kamaneeya Kalaga, Kayla Reiman


####################
# Import Libraries #
####################
import pandas as pd
from bs4 import BeautifulSoup


############################
# Read Oscar Data from CSV #
############################

###Dataset 1 of 4: Pictures###
#Create dataframe from csv
OscarsPictures = pd.read_csv('pictures.csv')

#View column names as a list
print(OscarsPictures.columns)

#View movie titles for first 5 observations
print(OscarsPictures['name'].head())
