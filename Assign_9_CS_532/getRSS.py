import requests
from lxml import etree


header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Accept-Language':'en'}
URL=[]
file=open('cyclefile.txt', 'r')
for line in file:
    URL.append(line.rstrip())
count=0
for url in URL:
    page=requests.get(url, headers=header, allow_redirects=True, stream=True)
    out=open('feeds/RSSfeed'+str(count)+'.xml', 'w')
    out.write(page.text)
    count+=1
    
        
        
