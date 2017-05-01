import feedparser
import re
from math import sqrt
from scipy import spatial
import os
import requests
from urllib.parse import urljoin
from datetime import datetime
import json

#Q1 functions
def cosine(vec1, vec2):
    return float(1-spatial.distance.cosine(vec1,vec2))
    


def getdistances(data,vec1):
    distancelist=[]
    for key in data.keys():
        vec2=data[key]
        distancelist.append((cosine(vec1,vec2),key))
    distancelist.sort(reverse=True)
    return distancelist

def knnestimate(data,vec1,k=3):
    # Get sorted distances
    dlist=getdistances(data,vec1)
    avg=float(0.0)
    # Take the average of the top k results
    for i in range(k):
        idx=dlist[i][0]
        print('\t%s'% dlist[i][1])
        avg+=idx
    avg=avg/k
    return avg


def readfile(filename):
    lines=[line for line in open(filename, 'r')]
    # First line is the column titles
    colnames=lines[0].strip( ).split('\t')[1:]
    rownames=[]
    data=[]
    for line in lines[1:]:
        p=line.strip( ).split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames,colnames,data

#|||||||||||||||||||||||||||||||||||||||||
#Q2 functions


def myread(articles, path):
    entries=[]
    data={}
    words={}
    for file in os.listdir(path):
        feed=os.path.join(path, file)
        f=feedparser.parse(feed)
        for entry in f.entries:
            entries.append(entry)
    for entry in entries:
        if entry.title in articles.keys():
            wc=getwordcounts(entry)
            for key in wc.keys():
                words.setdefault(key,0)
                words[key]+=1
            data[entry.title]=wc
    #shortens word list to 1000 most used        
    wordtuple=[]
    for w,bc in words.items( ):
        #frac=float(bc)/len(articles)
        #if frac>0.1 and frac<.99:
        wordtuple.append((w, bc))
    wordtuple.sort(key=lambda x: x[1], reverse=True)
    wordlist=list(x[0] for x in wordtuple)
    if len(wordlist)>1000:
        del wordlist[1000:]
    del wordtuple
    del words
    #converts wordcounts to a vector
    for title, d in data.items():
        vector=[]
        for word in wordlist:
            if word in d:
                vector.append(d[word])
            else: vector.append(0)
        data[title]=vector
    print('Total Number of Words: %d' %len(wordlist))
            
    return data
    

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(entry):
    wc={}
    if 'summary' in entry:
        summary=entry.summary
    else:
        summary=entry.description
    # Extract a list of words
    words=getwords(entry.title+' '+summary)
    for word in words:
        wc.setdefault(word,0)
        wc[word]+=1
   
    return wc

def getwords(doc):
    splitter=re.compile('\\W*')
    # Split the words by non-alpha characters
    words=[s.lower( ) for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    # Return the unique set of words only
    return words

#|||||||||||||||||||||||||||||||||||||||||
#Question 3

def get_aggregate(uri):
    aggregate='http://memgator.cs.odu.edu/timemap/link/'.rstrip()
    uri=aggregate+uri.rstrip()
    tbody=requests.get(uri)
    print(tbody.status_code)
    if not(tbody.status_code == 200):
        raise StopIteration
    for line in tbody:
        yield line
                
def get_data(uri):
    num_mementos=0
    for line in get_aggregate(uri):
        if b'memento' in line:
            num_mementos+=1
    return num_mementos







