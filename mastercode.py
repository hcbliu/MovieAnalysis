#This is Kayla's current version

##################
# Movie Analysis #
##################
#Authors: Sinduja Sriskanda, Hui-Chen Betty Liu, Kamaneeya Kalaga, Kayla Reiman

####################
# Import Libraries #
####################
import pandas as pd
from bs4 import BeautifulSoup

#################################
# Read Award Datasets from CSVs #
#################################

#Create dataframe from https://www.kaggle.com/fmejia21/demographics-of-academy-awards-oscars-winners/data  
#KR 2.21.20: Added engine = 'python' based on kaggle discussion:
  #https://www.kaggle.com/paultimothymooney/how-to-resolve-a-unicodedecodeerror-for-a-csv-file
OscarsDemo = pd.read_csv('Datasets\Oscars-demographics-DFE.csv', engine = 'python')

#Create dataframes from https://www.kaggle.com/rounakbanik/the-movies-dataset#credits.csv
#Preceding these w/ m because they came from the folder called "the movies dataset"
m_credits = pd.read_csv(r'Datasets\the-movies-dataset\credits.csv', engine = 'python')
m_metadata = pd.read_csv(r'Datasets\the-movies-dataset\movies_metadata.csv', engine = 'python')

print('Attributes of the m_credits dataset: ', m_credits.columns)

#view the cast entry for the first movie:
print(m_credits.cast[0])
#KR note to teammates: can anyone figure out how to translate this to a list of names?
#My understanding (just based only seeing "buzz lightyear" credited) is that the first
#movie on the credits list is Toy Story. The cast field for Toy Story returns
#a list of cast members, along with their genders and some other info. Most of this
#information is irrelevant to us.
