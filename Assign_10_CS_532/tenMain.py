from ten_dimension import *
from libsvm.python import svm
from libsvm.python import svmutil as svmu
import feedparser
import os



#Question 1
(rownames, colnames, vectors)=readfile('blogdata.txt')

data=dict(zip(rownames, vectors))

Vec={}
klist=[1,2,5,10,20]
for key, value in data.items():
    if key == 'F-Measure':
        Vec.setdefault(key, value)
    if key == 'Web Science and Digital Libraries Research Group':
        Vec.setdefault(key, value)
for key in Vec.keys():
    del data[key]


for key, value in Vec.items():
    for k in klist:
        print('Nearest Neighbors to %s for k=%d' % (key, k))
        print('Avg Distance %f' % knnestimate(data, value, k))
        
del data, Vec, klist, rownames, colnames, vectors

#|||||||||||||||||||||||||||||||||||||||||||||||
#Question 2
articles={}
categories=[]
for line in open('groundtruth.txt', 'r'):
    (title, actual)=line.split('\t')
    articles.setdefault(title,actual.rstrip())
    if actual.rstrip() not in categories:
        categories.append(actual.rstrip())

data=myread(articles, './feeds')
for cat in categories:
    vectors=[]
    answers=[]
    for title, answer in articles.items():
        if answer==cat:
            answers.append(1)
        else:
            answers.append(-1)
        vectors.append(data[title])
    prob=svm.svm_problem(answers, vectors)
    param=svm.svm_parameter('-t 2 -v 10')
    
    correct=svmu.svm_train(prob, param)
    print('Category: %s \n\t Percent Correct: %d' %(cat, correct))    
    
#||||||||||||||||||||||||||||||||||||||||||||||
#Question 3

old_data=[]
with open("old_data_set.txt", 'r') as olddata:
    for line in olddata:
        old_data.append(line.split('\t')[0].rstrip())
links=[]
with open('twitter_links.txt', 'r') as linkfile:
    for line in linkfile:
        links.append(line.rstrip())

data=dict(zip(links, old_data))

with open('data_set.txt', 'w') as outfile:
    for key, value in data.items():
        new_count=get_data(key)
        print(value, new_count, (int(new_count)-int(value)), sep='\t', file=outfile)
        




    
