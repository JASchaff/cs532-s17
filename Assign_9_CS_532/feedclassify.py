import requests
from fishermethod import *
import feedparser
import os




articles={}
#establish ground truth, if not already done
if not os.path.isfile('./groundtruth.txt'):
    listarticles=downtohundred('./feeds')
    with open('groundtruth.txt', 'w') as gtout:
        print('Establishing Ground Truth: %d'% len(articles))
        for a in listarticles:
            print(a[0], a[1], sep=': ')
            cat=input('Enter category: ')
            print(a[0], cat, sep='\t', file=gtout)
            articles.setdefault(a[0],cat)

else:
    for line in open('groundtruth.txt', 'r'):
        (title, actual)=line.split('\t')
        articles.setdefault(title,actual.rstrip())
        
#process for question 2
#halfone=dict(list(articles.items())[:50])
#halftwo=dict(list(x for x in articles.items() if x not in halfone.items()))
#cl=fisherclassifier(getwords)
#if not os.path.isfile('./cyclingdb.db'):
#    cl.setdb('cyclingdb.db')
#    myread(halfone, './feeds', cl)
#else: cl.setdb('cyclingdb.db')
#myclassify(halftwo, './feeds', cl)
#del cl

#process for question 3
#cl2=fisherclassifier(getwords)
#halfninety=dict(list(articles.items())[:90])
#halften=dict(list(x for x in articles.items() if x not in halfninety.items()))
#if not os.path.isfile('./cyclingdb2.db'):
#    cl2.setdb('cyclingdb2.db')
#    myread(halfninety, './feeds', cl2)
#else:cl2.setdb('cyclingdb2.db')
#myclassify(halften, './feeds', cl2)
#del cl2

#process for question 4
tenoften={}
topcount=dict(list(x for x in articles.items()))
downcount=dict(list(x for x in articles.items())[:90])
downcounter=90
for i in range(10):
    tenoften[i]=dict(list(x for x in topcount.items() if x not in downcount.items()))

    downcounter-=10
    #try:
    downcount=dict(list(downcount.items())[:downcounter])
    #except:
        #print('TEN OF TEN: %d' % len(tenoften))
        #break
    topcount=dict(list(x for x in topcount.items() if x not in tenoften[i].items()))
print('TEN OF TEN: %d' % len(tenoften))

for i in range(10):
    cl3=fisherclassifier(getwords)
    datafile=str('tenoften'.rstrip() +str(i)+'.db')
    if not os.path.isfile(os.path.join('./',datafile)):
        cl3.setdb(datafile)
        temp={}
        for keys in tenoften.keys():
            for key,item in tenoften[keys].items():
                if key not in tenoften[i].keys():
                    temp[key]=item
                    
        myread(temp, './feeds', cl3)
    else:cl3.setdb(datafile)
    print('Data Set %s' % str('tenoften'+ str(i)))
    myclassify(tenoften[i],'./feeds',cl3)
    
               
    



        
        
        
        
