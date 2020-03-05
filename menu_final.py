##################
# Movie Analysis #
##################
#Authors: Sinduja Sriskanda, Hui-Chen Betty Liu, Kamaneeya Kalaga, Kayla Reiman

#Import libraries
import pandas as pd
import numpy as np #for plotting
import matplotlib.pyplot as plt
import seaborn as sns

#Read in CSV: 
#Note: this CSV is the result of processing CSVs from Kaggle, web scraping
#from bechdeltest.org, and using an API.     
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
        try:
            c,name = searchmovie(name)
            if c >= 0:
                index = movie[movie['title'] == name].index[0]
                print('=============================================')
                print('Basic Information')
                print('=============================================')
                print('\nMovie title:')
                print(movie.iloc[index]['title'])
                print('\nYear of release:')
                print(movie.iloc[index]['year'])
                print('\nPlot summary:')
                print(movie.iloc[index]['synopsis'])
                print('\n=============================================')
                selection = menu()
                tableFunctions(selection, index)
                validtitle = False
            else:
                print("\nPlease enter a valid movie title!")
                continue
        except:
            print('\n')


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
    c = int(input("\nInput the corresponding number if one of the titles matches your movie or -1 to re-enter: "))
    if c < 0:
        return c,name
    else:
        try: 
            name = namelist[c]
            return c,name
        except:
            print('The number you entered was invalid. Please try again.')
 
    
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
        2. See cast gender information
        3. See crew gender information
        4. See summary of gender statistics across all movies
        5. Enter a different movie name
        0. Quit \n
    Enter '1' for the first option, '2' for the second option, and so on.
    \nEnter option: '''))
        print('\n')
        if selection not in range(0,6,1): 
            print('\n ERROR: try entering a number between 1 to 5 (or 0 to QUIT).')
            continue           
        else:
            validSelection = True
            return selection

#These display functions are used to work around the way that values are 
#coded as strings.
            
# displaypct()
# Parameters: pctstring, a percentage which is currently read as a string
# What it does: displays missing or converts to a float
# Returns: string with 'x%' or 'Missing' or 'Insufficient Sample'
def displaypct(pctstring):
    if pctstring == 'Missing':
        out = 'Missing'
    elif pctstring == 'insufficient sample':
        out = 'insufficient sample'
    else: 
        out = str(int(round(float(pctstring),2)*100)) + '%'
    return out

# displaypct()
# Parameters: intstring, an integer which is currently read as a string
# What it does: displays missing or converts to a float
# Returns: string with an int or 'Missing' or 'Insufficient Sample'
def displayint(intstring):
    if intstring == 'Missing':
        out = 'Missing'
    elif intstring == 'insufficient sample':
        out = 'insufficient sample'
    else: 
        out = int(float(intstring))
    return out

# tableFunctions()
# Parameters: s, an integer variable; index, an integer value
# What it does: it displays the information based on user input from menu selection
# Returns: none, just prints the information
def tableFunctions(s,index):
    valid = True
    while valid:
        if s == 1: 
            print('=============================================')
            print("Bechdel test results")
            print('=============================================')
            print("Score: ", movie.iloc[index]['bechdel_score'])
            print("\nDescription of the score: ", movie.iloc[index]['bechdel_desc'])
            try:
                plt.close() 
                bechdel_nonmiss = movie.bechdel_score[movie.bechdel_score != 'Missing'].apply(lambda x: int(x))
                n, bins, patches = plt.hist(bechdel_nonmiss,bins = np.arange(5)-0.5, color = 'silver')
                score = int(movie.iloc[index]['bechdel_score'])
                patches[score].set_fc('blue')
                plt.title('Bechdel Results in the Context of Full Dataset from bechdeltest.org')
                plt.xlabel('Score on Bechdel Test')
                plt.ylabel('Number of movies')
                plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                plt.xticks(np.arange(4))
                plt.show()
            except:
                print('\n')
            print('=============================================')
            
            s = menu()
        elif s == 2: 
            print('=============================================')
            print('Cast Gender Information')
            print('=============================================')
            print("Percentage of women in the cast: ", displaypct(movie.iloc[index]['cast_pct_women']))
            print("Cast members in dataset: ", displayint(movie.iloc[index]['cast_n']))            
            #pie plot for cast
            try:
                plt.close()
                plt.title('Gender Breakdown of the Cast in %s' %(movie.iloc[index]['title']))
                value = float(movie.iloc[index]['cast_pct_women'])
                values = [value, 1-value]
                mylabels=['Women','Men'] 
                plt.pie(values, labels=mylabels, colors = ('blue', 'silver'))
                plt.show()

                #histogram for cast
                if ((movie.iloc[index]['cast_pct_women'] != 'Missing') & (movie.iloc[index]['cast_pct_women'] != 'insufficient sample')) == True:
                    plt.close()
                    cast_nonmiss = movie.cast_pct_women[(movie.cast_pct_women != 'Missing') &\
                                                        (movie.cast_pct_women != 'insufficient sample')].\
                                                        apply(lambda x: float(x))
                    n, bins, patches = plt.hist(cast_nonmiss, color = 'silver', bins = 15)
                    for i in range(len(bins)):
                        if float(movie.iloc[index]['cast_pct_women']) > bins[i]:
                            bin_number = i
                    patches[bin_number].set_fc('blue')
                    plt.title('%s Cast Gender Ratio Compared to Other Movies' %(movie.iloc[index]['title']))
                    plt.xlabel('% women in the cast')
                    plt.ylabel('Number of movies')
                    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                    plt.xticks(rotation=70)
                    bins2 = list()
                    for i in bins:
                        bins2.append(str(round(i, 2)) + '%')
                    plt.xticks(bins, bins2)
                    plt.show()
            except:
                print("\n")
            print('=============================================')
            
            s = menu()
        elif s == 3: 
            print('=============================================')
            print('Crew Gender Information')
            print('=============================================')
            print("Percentage of women in the crew: ", displaypct(movie.iloc[index]['crew_pct_women']))
            print("Crew members in dataset: ", displayint(movie.iloc[index]['crew_n']))           
            #pie plot for crew
            try:
                plt.close()
                value = float(movie.iloc[index]['crew_pct_women'])
                plt.title('Gender Breakdown of the Crew in %s' %(movie.iloc[index]['title']))
                values = [value, 1-value]
                mylabels=['Women','Men'] 
                plt.pie(values, labels=mylabels, colors = ('blue', 'silver'))
                plt.show()
                if ((movie.iloc[index]['crew_pct_women'] != 'Missing') & (movie.iloc[index]['crew_pct_women'] != 'insufficient sample')) == True:
                    plt.close()
                    crew_nonmiss = movie.crew_pct_women[(movie.crew_pct_women != 'Missing') &\
                                                        (movie.crew_pct_women != 'insufficient sample')].\
                                                        apply(lambda x: float(x))
                    n, bins, patches = plt.hist(crew_nonmiss, color = 'silver', bins = 15)
                    for i in range(len(bins)):
                        if float(movie.iloc[index]['crew_pct_women']) > bins[i]:
                            bin_number = i
                    patches[bin_number].set_fc('blue')
                    plt.title('%s Crew Gender Ratio Compared to Other Movies' %(movie.iloc[index]['title']))
                    plt.xlabel('% women in the crew')
                    plt.ylabel('Number of movies')
                    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                    plt.xticks(rotation=70)
                    bins2 = list()
                    for i in bins:
                        bins2.append(str(round(i, 2)) + '%')
                    plt.xticks(bins, bins2)
                    plt.show()
            except:
                print("\n")            
            print('=============================================')
            
            
            s = menu()
        elif s == 4: 
            print('=============================================')
            print("Analysis Across Movies")
            print('=============================================')
            pd.set_option('mode.chained_assignment', None)
            
            yr = set()
            for i in movie.year[:]:
                yr.add(i)
            yr = list(yr)
            yr.sort()
            moviebt_nonmiss = movie[movie.bechdel_score != 'Missing']
            moviebt_nonmiss['bechdel_score'] = pd.to_numeric(moviebt_nonmiss['bechdel_score'])    
            
            # line graph showing the trend of average bechdel score throughout the years
            plt.close()
            plt.title('Average Bechdel Score over the years')
            plt.ylim(ymin=0, ymax=3)
            m, b = np.polyfit(moviebt_nonmiss['year'], moviebt_nonmiss['bechdel_score'], 1)
            plt.plot(moviebt_nonmiss['year'], m*moviebt_nonmiss['year'] + b, color='r', linestyle = '--')
            plt.plot(moviebt_nonmiss.groupby('year').mean()['bechdel_score'], color='purple')
            plt.show()
            print('The average Bechdel test scores are increasing slightly over time.')
            print('=============================')
            
            # line graphs showing trends for average cast and crew percentages throughout the years
            moviecast_nonmiss = movie[(movie.cast_pct_women != 'Missing') & (movie.cast_pct_women != 'insufficient sample')]
            moviecast_nonmiss['cast_pct_women'] = pd.to_numeric(moviecast_nonmiss['cast_pct_women'])*100    

            plt.close()
            plt.title('Average percentage of women in cast over the years')
            plt.ylim(ymin=0, ymax=100)
            plt.axhline(y=50, color='r', linestyle='--')
            m, b = np.polyfit(moviecast_nonmiss['year'], moviecast_nonmiss['cast_pct_women'], 1)
            plt.plot(moviecast_nonmiss['year'], m*moviecast_nonmiss['year'] + b, color='mediumblue', linestyle = ':')
            plt.plot(moviecast_nonmiss.groupby('year').mean()['cast_pct_women'], color = 'forestgreen')
            plt.show()
            print('The average percentage of women in the cast looks to be increasing very slightly over the years, although it is below the desired line.')
            print('There is a sudden increase in the last 5 years, and the percentage has reached 50 in 2017')
            print('=============================')
            
            moviecrew_nonmiss = movie[(movie.crew_pct_women != 'Missing') & (movie.crew_pct_women != 'insufficient sample')]
            moviecrew_nonmiss['crew_pct_women'] = pd.to_numeric(moviecrew_nonmiss['crew_pct_women'])*100    

            plt.close()
            plt.title('Average percentage of women in crew over the years')
            plt.ylim(ymin=0, ymax=100)
            plt.axhline(y=50, color='r', linestyle='--')
            m, b = np.polyfit(moviecrew_nonmiss['year'], moviecrew_nonmiss['crew_pct_women'], 1)
            plt.plot(moviecrew_nonmiss['year'], m*moviecrew_nonmiss['year'] + b, color='limegreen', linestyle = ':')
            plt.plot(moviecrew_nonmiss.groupby('year').mean()['crew_pct_women'], color = 'blueviolet')
            plt.show()
            pd.reset_option('mode.chained_assignment')
            print('The average percentage of women in crew looks to be increasing over the years, although it is below the desired line at 50%.')
            print('The data show a drastic decrease in percentage of women in the crew data in last 5 years. This may be due to missing data, so additional analyses would be needed to draw conclusions about this.')
            print('=============================')
            
            #  Correlation and pairgrid to compare the average percentage for cast and crew
            movie_nonmiss = pd.DataFrame()
            crew = list(moviecrew_nonmiss.groupby('year').mean()['crew_pct_women'])
            cast = list(moviecast_nonmiss.groupby('year').mean()['cast_pct_women'])
            cast.append(0)
            movie_nonmiss['year'] = yr
            movie_nonmiss['Avg_cast_pct'] = cast
            movie_nonmiss['Avg_crew_pct'] = crew
            
            plt.close()
            corCoeff = str(round( movie_nonmiss['Avg_cast_pct'][:28].corr(movie_nonmiss['Avg_crew_pct'][:28]), 2)) 
            plt.title('Linear regression, correlation = ' + corCoeff)
            sns.regplot(x='Avg_cast_pct', y='Avg_crew_pct', data=movie_nonmiss[:28])
            sns.pairplot(data=movie_nonmiss[['Avg_cast_pct','Avg_crew_pct']])
            plt.ylabel('Average % women in the crew')
            plt.xlabel('Average % women in the cast')
            plt.show()
            print('There a positive relationship between the percentages of women the cast and crew, but the correlation is very low due to an outlier.')
            print('=============================================')     
            
            s = menu()
            
        elif s == 5:
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
                s = 5
        elif s == 0:
            print("\nThank You! Hope you enjoyed this application!")
            valid = False
            

# inside this we get the dataframe used for every function 
# Returns: basic information of the movie
if __name__ == '__main__':
    main()
    
    
