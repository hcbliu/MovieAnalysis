##################
# Movie Analysis #
##################
#Authors: Sinduja Sriskanda, Hui-Chen Betty Liu, Kamaneeya Kalaga, Kayla Reiman

#Note: This code was written by Betty and adapted by Kamaneeya as of 2.27.20
#Minor edits from Kayla on 2.28.20


#KR note: added this to the top b/c easier to update
#Import libraries
import pandas as pd

#Read in CSV:     
movie = pd.read_csv("cleanedMovieData_20200228_9am.csv") #Update this as needed


#Troubleshooting option for programmer: view dataset

#def viewdata(dsname, desc = 'add description here'):
#    name =[x for x in globals() if globals()[x] is dsname][0]
#    print('------------------------------------------------------')
#    print('THREE-PART OVERVIEW OF DATASET: ', name.upper())
#    print('Description:', desc)
#    print('  1. Columns and data types in %s\n' %(name), dsname.dtypes)
#    print('  2. Shape of dataframe:', dsname.shape)
#    print('\n  3. Use head() to see 5 Rows')
#    print(dsname.head(), end = '\n') 
#    
#viewdata(movie, 'This is the data that will be used for the app.')

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
        name = input("Please enter a movie name: ")
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
    print("Did you mean any of the following?")
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
            print("Cast members in dataset: ", movie.iloc[index]['cast_n'][0:2])
            print('=============================') 
            s = menu()
        elif s == 3: 
            print("Summary statistics:")
            print('=====================')
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