##################
# Movie Analysis #
##################
#Authors: Sinduja Sriskanda, Hui-Chen Betty Liu, Kamaneeya Kalaga, Kayla Reiman

#Note: This code was written by Betty and adapted by Kamaneeya as of 2.27.20
#Minor edits from Kayla on 2.28.20
#Additional edits from Kayla on 3.3.20 as of 2pm


#KR note: added this to the top b/c easier to update
#Import libraries
import pandas as pd
import numpy as np #for plotting
import matplotlib.pyplot as plt
import seaborn as sns


#Read in CSV:     
movie = pd.read_csv("cleanedMovieDataFINAL.csv") #Version from Betty as of Feb 29, 2020, 10:38 PM

#Troubleshooting option for programmer: view dataset
#def viewdata(dsname, desc = 'add description here'):
#    name =[x for x in globals() if globals()[x] is dsname][0]
#    varlist = [name + '["' + dsname.columns[i] + '"]'for i in range(len(dsname.columns))]
#    print('------------------------------------------------------')
#    print('THREE-PART OVERVIEW OF THE DATASET CALLED %s:' %(name.upper()))
#    print('Description: %s is %s' %(name, desc))
#    print('\n  1. Columns in %s:' %(name))
#    print(('%-20s %-20s %-30s') %('VAR NAME', 'TYPE OF COLUMN', 'TYPE OF FIRST CELL'))
#    for i in range(len(dsname.columns)):
#        print(('%-20s %-20s %-30s') %(dsname.columns[i], dsname.dtypes[i], \
#              type(eval(varlist[i])[0])), end ='\n')
#    print('   2. Shape of dataframe:', dsname.shape)
#    print('   3. Use head() to see 5 Rows')
#    print(dsname.head(), end = '\n') 
#    
#viewdata(movie, 'our main dataset.') 

# main()
# Parameters: none
# What it does: prompts the user to enter a movie name as input, 
# calls on searchnames function
# to find potential matches and ones the name is selected, in prints the 
# basic information and calls menu and tableFunctions functions 
# Returns: basic information of the movie

def main(): 
    validtitle = True
    while validtitle:
        name = input("Please enter a movie name (or part of a movie name): ")
        c,name = searchmovie(name)
        if c >= 0:
            index = movie[movie['title'] == name].index[0]
            print('\nMovie title:')
            print('==============')
            print(movie.iloc[index]['title'])
            print('\nYear of release:')
            print('==================')
            print(movie.iloc[index]['year'])
            print('\nPlot summary:')
            print('=============')
            print(movie.iloc[index]['synopsis'])
            selection = menu()
            tableFunctions(selection, index)
            validtitle = False
        else:
            print("\nPlease enter a valid movie title!")
            continue


# searchmovie()
# Parameters: name (entered by user)
# What it does: uses the movie name from input, uses regular expressions to
# find different possible movies that match the string entered and prompts
# the to choose which one they want.
# Returns: movie title and an int value c (not of high significance - just for 'if' statement)
def searchmovie(name):
    import re
    name_re = name + '|' + name.title() + '|' + name.upper() + '|' + name.lower() + '|' + name.swapcase() + '|' + name.upper().replace(' ','') + '|' + name.lower().replace(' ','') + '|' + name.swapcase().replace(' ','') + '|' + name.title().replace(' ','')
    i=0
    namelist =[]
    tlist = [movie['title'][i] for i in range(len(movie))]       
    print("\nIs your movie one of the following?")
    for t in tlist: 
        if re.search(name_re,t) != None:
            print(i,'-', t)
            i += 1
            namelist.append(t)
    c = int(input("\nSelect any one of the above matches or -1 to re-enter!"))
    if c < 0:
        return c,name
    else:
        name = namelist[c]
        return c,name
 
    
# menu()
# Parameters: none
# What it does: it prompts the user to input an integer between 1 and 4
# Returns: selection, an integer variable
def menu(): 
    validSelection = False
    while not validSelection:
        selection = int(input('''
        Choose one of the following options: \n
        1. See Bechdel Test scores.
        2. See crew and cast information
        3. See other summary statistics
        4. Enter a different movie name

        0. Quit \n
    Enter '1' for the first option, '2' for the second option, and so on.
    \nEnter option: '''))
        print('\n')
        if selection not in range(0,5,1): 
            print('\n ERROR: try entering a number between 1 to 4 (or 0 to QUIT).')
            continue           
        else:
            validSelection = True
            return selection

#KR note: This function will be used inside tableFunctions
# displaypct()
# Parameters: pctstring, a percentage which is currently read as a string
# What it does: displays missing or converts to a float
# Returns: string with 'x%' or 'Missing'
def displaypct(pctstring):
    if pctstring == 'Missing':
        out = 'Missing'
    else: 
        out = str(int(round(float(pctstring),2)*100)) + '%'
    return out

# tableFunctions()
# Parameters: s, an integer variable; index, an integer value
# What it does: it displays the information based on user input from menu selection
# Returns: none, just prints the information
def tableFunctions(s,index):
    valid = True
    while valid:
        if s == 1: 
            print("Bechdel test results:")
            print('=======================')
            print("Score: ", movie.iloc[index]['bechdel_score'])
            print("\nDescription of the score: ", movie.iloc[index]['bechdel_desc'])
            print('========================')
            s = menu()
        elif s == 2: 
            print('Cast and Crew information:')
            print('============================')
            print("Percentage of women in the crew: ", displaypct(movie.iloc[index]['crew_pct_women']))
            print("Crew members in dataset: ", movie.iloc[index]['crew_n'])
            print("Percentage of women in the crew: ", displaypct(movie.iloc[index]['cast_pct_women']))
            print("Cast members in dataset: ", movie.iloc[index]['cast_n'][0:2]) #this assumes no more than 99 cast members
            print('=============================') 
            s = menu()
        elif s == 3: 
            print("Summary statistics:")
            print('=====================')
            plt.close() 
            bechdel_nonmiss = movie.bechdel_score[movie.bechdel_score != 'Missing'].apply(lambda x: int(x))
            n, bins, patches = plt.hist(bechdel_nonmiss, color = 'g')
            #patches[int(score)].setfc('r') #KR note: why doesn't this work? It works in the example below!
            plt.title('Hisogram of Test Scores from bechdeltest.org')
            plt.xlabel('Score on Bechdel Test')
            plt.ylabel('Number of movies')
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
            plt.xticks(np.arange(4))
            plt.show()
            print('=====================')
            s = menu()
        elif s == 4:
            name = input("Enter a different movie name: ")
            c,name = searchmovie(name)
            if c >= 0:
                index = movie[movie['title'] == name].index.item()
                print('\nMovie title:')
                print('==============')
                print(movie.iloc[index]['title'])
                print('\nYear of release:')
                print('==================')
                print(movie.iloc[index]['year'])
                print('\nPlot summary:')
                print('=============')
                print(movie.iloc[index]['synopsis'])
                s = menu()
            else:
                print("\nPlease enter a valid movie title!")
                s = 4
        elif s == 0:
            print("\nThank You! Hope you enjoyed this application!")
            valid = False
            

# inside this we get the dataframe used for every function 
# Returns: basic information of the movie
if __name__ == '__main__':
    main()
    
    
#Testing Bechdel code

#plt.close() 
#bechdel_nonmiss = movie.bechdel_score[movie.bechdel_score != 'Missing'].apply(lambda x: int(x))
#n, bins, patches = plt.hist(bechdel_nonmiss, color = 'g')
##patches[2].setfc('r') #KR note: why doesn't this work? It works in the example below!
#plt.title('Hisogram of Test Scores from bechdeltest.org')
#plt.xlabel('Score on Bechdel Test')
#plt.ylabel('Number of movies')
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#plt.xticks(np.arange(4))
#plt.show()


#Example of coloring a rectangle in a histogram
#import numpy as np
#import matplotlib.pyplot as plt
#values =  np.random.randint(51, 140, 1000)
#n, bins, patches = plt.hist(values, bins=np.arange(50, 140, 2), align='left', color='g')
#patches[40].set_fc('r')
#plt.show()
