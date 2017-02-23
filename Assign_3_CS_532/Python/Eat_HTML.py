import hashlib
import requests
import os
from sys import argv
import bs4

class html_downloader():
    #converts URL to a filename ending in a provided extension
    def URL_to_filename(self, address, extension='.html'):
        m=hashlib.sha224(str(address).encode('utf-8')).hexdigest()
        filename=m.rstrip()+extension
        print(filename)
        return filename
    
    #pulls the page and processes it through process_page(tpage)
    def pull_page(self, address):
        address=address.rstrip()
        header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        tpage=requests.get(address, headers=header, allow_redirects=True)
        return tpage
        
    

if __name__ == '__main__':
    infilename=argv[1]
    h=html_downloader()
    filepath='HTML_pages/'
    directory=os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #a table with URLs and their hashed filenames
    with open('HTML_pages/hash_table.txt', 'a') as hashtable:
        #the list of URLs
        with open(infilename, 'r') as infile:
            for URL in infile:
                try:
                    tpage=h.pull_page(URL)
                    tname=h.URL_to_filename(URL, '.html')
                    hashtable.write(tname.rstrip()+'\t'+ URL)
                    tname=filepath.rstrip()+tname
                    tfile=open(tname, 'w')
                    tfile.write(tpage.text)
                except:
                    print('URL failed: ' + URL)
                    pass
            
