from sevenhtml import *
from math import log2, log10, floor
import sys


round_to_n=lambda x, n: round(x, -int(floor(log10(abs(x))))+(n-1))
apcount={}
wordcounts={}
for feedurl in open('lurl.txt'):
    try:
        (title, wc)=getwordcounts(feedurl)
    except KeyError:
        sys.stdout.write('Key Error on %s' % feedurl)
        continue
    sys.stdout.write('\r%d URL: %s'% (len(wordcounts), feedurl))
    sys.stdout.flush()
    wordcounts[title]=wc
    for word,count in wc.items( ):
        apcount.setdefault(word,0)
        apcount[word]+=1
    if len(wordcounts)==100:
        break

wordtuple=[]
for w,bc in apcount.items( ):
    frac=float(bc)/len(wordcounts)
    if frac>0.1 and frac<0.5:
        wordtuple.append((w, frac))
wordtuple.sort(key=lambda x: x[1], reverse=True)
wordlist=list(x[0] for x in wordtuple)
if len(wordlist)>1000:
    del wordlist[1000:]
print('Number of Words: %d' % len(wordlist))
print(*wordlist, sep='\n')
del wordtuple

#this section is added for TFIDF scores
#|||||||||||||||||||||||||||||||||||||
for blog,wc in wordcounts.items():
    totalwords=sum(wc.values())
    for word in wordlist:
        if word in wc:
            wc[word]=(wc[word]/float(totalwords))*(log2(len(wordcounts)/float(apcount[word])))
#|||||||||||||||||||||||||||||||||||||
out=open('2blogdata.txt','w')
out.write('Blog')

for word in wordlist:
    out.write('\t%s' %word)
out.write('\n')
for blog, wc in wordcounts.items():
    out.write(blog)
    for word in wordlist:
        if word in wc:
            out.write('\t%f' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')


