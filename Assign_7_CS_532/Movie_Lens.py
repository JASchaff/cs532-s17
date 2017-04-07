from recommendations import *
import sys
import json

#question 1: collects user information for comparison
users=loadDemographics()
age=input('Enter age: ')
gender=input('Enter gender: ')
occupation=input('Enter most correct occupation from list {technician, writer, executive, administrator, student, lawyer, educator, scientist, entertainment, programmer, librarian, homemaker, engineer, artist, marketing, healthcare, doctor, retired, salesman, none, other}: ')
#asks for the number of returned results the user wants. I did this because the top 3 were not good matches
results=int(input('Enter number of results required: '))
user={'age': age, 'gender': gender, 'occupation':occupation}
alike=compareDemographics(users, user)
alike_sorted= sorted(alike.items(), key=lambda x: x[1], reverse=True)

m_alike=list(alike_sorted[x][0] for x in range(results))
print(*m_alike, sep='\t')

del users
del alike

prefs=loadMovieLens()
#prints likely candidates and their preferences
for u in m_alike:
    temp=sorted(prefs[u].items(), key=lambda x: x[1], reverse=True)
    print(u+'\n', 'Top 3:\n', temp[:3], '\n\tBottom 3:\n', temp[-3:], sep='\t')

del m_alike
#user selects candidate most like them in movie preferences
a_user=input('Select the user most like you: ')
#Question 2: finds top 5 and bottom 5 correlations to candidate selected 
top=topMatches(prefs, a_user)
bottom=bottomMatches(prefs, a_user)
print('Top Matches:\n', *top, '\n', sep='\t')
print('Bottom Matches:\n', *bottom, '\n', sep='\t')
#Question 3: finds top 5 movie recommendations and top 5 movies not to watch
rankings=getRecommendations(prefs, a_user)
print('Top 5 Movies to Watch:\n', rankings[:5], '\nTop 5 Movies Not to Watch:\n', rankings[-5:], sep='\t')

del a_user, top, bottom, rankings
#Question 4: get matches from personal fav and hate from the list
fav=input('Enter your favorite Movie from the List: ')
hate=input('Enter your least favorite Movie from the List: ')

items=transformPrefs(prefs)
favtop=topMatches(items, fav)
favbottom=bottomMatches(items, fav)
hatetop=topMatches(items, hate)
hatebottom=bottomMatches(items, hate)
print(fav+' Top 5:\n', *favtop, '\n'+fav+' Bottom 5:\n', *favbottom, sep='\t')
print(hate+' Top 5:\n', *hatetop, '\n'+hate+' Bottom 5:\n', *hatebottom, sep='\t')

#lensrank=lensMovieRank(items)
#with open('Data/lensrank.txt', 'w') as out:
    #for key, value in lensrank.items():
        #print(key, value, sep='\t', file=out)
#movies=loadMovies()

