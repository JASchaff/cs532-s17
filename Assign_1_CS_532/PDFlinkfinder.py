import requests
from bs4 import BeautifulSoup
import lxml
import sys
from urllib.parse import urljoin


if not(len(sys.argv)==2):
    raise ValueError("Missing or multiple arguments")
address=sys.argv[1]
if not (address.startswith("http://") or address.startswith("https://")):
    raise ValueError("Argument not an URI")
page=requests.get(address, allow_redirects=True)
soup=BeautifulSoup(page.content, "lxml")
linklist=[]
pdflinklist=[]

numlinks=0
numpdfs=0
rellinks=0
unhandledlinks=0;
for link in soup.find_all('a'):
    linklist.append(link.get('href'))
    numlinks+=1
print("Number of links found: ", numlinks)
for i in linklist:
    if not i:
        unhandledlinks+=1
        continue
    if (i.startswith("http://") or i.startswith("https://")):
        #try:
        tpage=requests.get(i, allow_redirects=True, stream=True)
        temp=tpage.headers.get('content-type')
        if "pdf" in temp:
            if len(tpage.history) == 0:
                pdflinklist.append((i, "No Redirect", tpage.headers.get('content-length')))
            else:
                pdflinklist.append((i, tpage.url, tpage.headers.get('content-length')))
            numpdfs+=1
        tpage.close
        #except Exception:
            #unhandledlinks+=1
            #pass
    else:
        try:
            reladd=urljoin(address, i)
            tpage=requests.get(reladd, allow_redirects=True, stream=True)
            temp=page.headers.get('content-type')
            if "pdf" in temp:
                if len(tpage.history) == 0:
                    pdflinklist.append((reladd, "No Redirect", tpage.headers.get('content-length')))
                else:
                    pdflinklist.append((reladd, tpage.url, tpage.headers.get('content-length')))
                numpdfs+=1
            tpage.close
        except Exception:
            unhandledlinks+=1
            pass
        rellinks+=1
print("Number of links to pdfs found: ", numpdfs)
print("Number of relative links found: ", rellinks)
print("Number of unhandled links: ", unhandledlinks)
for i in pdflinklist:
    print ("\t\t".join(i))

