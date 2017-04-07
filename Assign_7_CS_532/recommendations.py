from math import sqrt
from sys import stdout
import os
#import requests
#import bs4

# Returns a distance-based similarity score for person1 and person2


def sim_distance(prefs,person1,person2):
    # Get the list of shared_items
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
            # if they have no ratings in common, return 0
            if len(si)==0:
                return 0
            # Add up the squares of all the differences
            sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                                for item in prefs[person1] if item in prefs[person2]])
            return 1/(1+sum_of_squares)

def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    # Find the number of elements
    n=len(si)

    # if they are no ratings in common, return 0
    if n<20: return 0
        
    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
        
    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
        
    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
        
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        
    if den==0: return 0
        
    r=num/den
    return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]
    # Sort the list so the highest scores appear at the top
    scores.sort(key=lambda x: x[0])
    scores.reverse( )
    return scores[:n]

def bottomMatches(prefs, person, n=5, similarity=sim_pearson):
    scores=[(similarity(prefs, person, other), other)
            for other in prefs if other!=person]
    scores.sort(key=lambda x: x[0])
    return scores[:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person:
            continue
        sim=similarity(prefs,person,other)

        # ignore scores of zero or lower
        if sim<=0:
            continue
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    # Create the normalized list
    rankings=[(total/simSums[item],item)
              for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort(key=lambda x: x[0])
    rankings.reverse( )
    return rankings


def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person]=prefs[person][item]
            
    return result


def initializeUserDict(tag,count=5):
    user_dict={}
    # get the top count' popular posts
    for p1 in get_popular(tag=tag)[0:count]:
        # find all users who posted this
        for p2 in get_urlposts(p1['href']):
            user=p2['user']
            user_dict[user]={}
    return user_dict



def calculateSimilarItems(prefs,n=10):
    # Create a dictionary of items showing which other items they
    # are most similar to.
    result={}
    # Invert the preference matrix to be item-centric
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # Status updates for large datasets
        c+=1
        if c%100==0:
            print("%d / %d" % (c, len(itemPrefs)))
        # Find the most similar items to this one
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result


def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    # Loop over items rated by this user
    for (item,rating) in userRatings.items( ):
        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            # Ignore if this user has already rated this item
            if item2 in userRatings:
                continue
            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
    # Divide each total score by total weighting to get an average
    rankings=[(score/totalSim[item],item)
              for item,score in scores.items( )]
    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings


def loadMovieLens(path='data/'):
    # Get movie titles
    movies={}
    for line in open(path +'u.item', encoding='latin-1'):
        (id_,title)=line.split('|')[0:2]
        movies[id_]=title
    # Load data
    prefs={}
    for line in open(path +'u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs


def loadDemographics(path='data/'):
    #get user data
    users={}
    for line in open(path +'u.user'):
        (id_, age, gender, occupation, zip_)=line.split('|')
        users[id_]={'age': age, 'gender': gender, 'occupation': occupation}

    return users

def compareDemographics(users, user):
        alike={}
        for key in users:
            score=0
            score+= 2*(10-abs(int(users[key]['age']) - int(user['age'])))
            if users[key]['gender'].lower()==user['gender'].lower():
                score+=20
            else: score+=10
            if users[key]['occupation'].lower()==user['occupation'].lower():
                score+=20
            else: score+=10
            alike[key]=score
        return alike

def loadMovies(path='data/'):
    #get movie data
    movies={}
    for line in open(path+'u.item'):
        (id_,title, date, url)=line.split('|')[0:4]
        movies[title]=url
    return movies

#returns a normalized rank value
def lensMovieRank(items):
    lensrank={}
    temprank=[]
    for key in items.keys():
        den=float(0)
        ranking=sum([int(x) for x in items[key].values()])
        den=len(items[key].keys())
        ranking=(ranking/den)/float(5)
        lensrank[key]=ranking
    return lensrank


#def IMDB_Rank(movies):
 #   IMDBrank={}
 #   for key in movies.keys():
        
    
    
def pull_page(address):
    address=address.rstrip()
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    tpage=requests.get(address, headers=header, allow_redirects=True)
    return tpage








    
