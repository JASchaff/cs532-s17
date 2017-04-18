from sevenhtml import *
import os



lurl=[]
if os.path.isfile('lurl.txt'):
    for line in open('lurl.txt', 'r'):
        lurl.append(line.rstrip())

else:
    lurl.extend(('http://f-measure.blogspot.com/feeds/posts/default?alt=rss', 'http://ws-dl.blogspot.com/feeds/posts/default?alt=rss'))
    out=open('lurl.txt', 'w')
    print(*lurl, sep='\n', file =out)
    out.close()
    
with open('lurl.txt', 'a')as app:
    while len(lurl) is not 125:
        turl=get_random_blog('en')
        if turl.rstrip() not in lurl:
            lurl.append(turl.rstrip())
            print(turl, file=app)





    
