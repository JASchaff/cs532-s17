import mmap
from sys import argv
import os
import requests
from bs4 import BeautifulSoup
import argparse
from math import log2, log10, floor
import re

#searches a directory for files containing a search term
class search_dir():
    def files_contain(self, directory, search_term):
        file_list=[]
        empty_file=0
        total_file=0
        for filename in os.listdir(directory):
            try:
                if filename.endswith('.txt') and not filename.startswith('hash'):
                    print(filename)
                    filepath=os.path.join(directory, filename)
                    total_file+=1
                    if self.meets(filepath, search_term):
                        file_list.append(filepath)
            except:
                empty_file+=1
                URL=self.get_orig_URL( (os.path.splitext(filename)[0].rstrip() + '.html'), os.path.join(directory, 'hash_table.txt'))
                print('Empty File count: ', empty_file, '\tUsable File count: ', total_file-empty_file, '\nURL: ', URL)
                pass
        print('Empty File count: ', empty_file, '\tUsable File count: ', total_file-empty_file)
        return file_list
                    
    def meets(self, filepath, search_term):
        with open(filepath, 'r+b', 0) as file, \
             mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(bytes(search_term, 'utf-8')) != -1:
                return True
            return False
    def get_orig_URL(self, filename, hash_table_file_path):
        with open(hash_table_file_path, 'r') as hash_file:
            #print('search for: ', filename)
            for line in hash_file:
                fields=line.split('\t')
                if fields[0]== filename:
                    return fields[1]
            return 'oops'
        
        
#analyzes a stripped html file for TF = #search_term/#words
#and also searches google for search term and returns IDF=search_results/size_of_index                     
class corpus_analysis():
    def get_TF(self, filepath, search_term):
        term_count=0
        word_count=0
        with open(filepath, 'r') as file:
            for line in file:
                words=line.split()#re.findall('[a-zA-Z_]+',line)
                word_count+=len(words)
                for i in words:
                    if search_term in i:
                        term_count+=1
            return term_count/word_count

    def get_IDF(self, search_term):
        #this number came from http://www.statisticbrain.com/total-number-of-pages-indexed-by-google/
        google_index=30000000000000
        parser = argparse.ArgumentParser(description='Get Google Count.')
        parser.add_argument('--word', help='word to count')
        args = parser.parse_args(['--word=search_term'])
        #pulls the google search results
        r = requests.get('http://www.google.com/search',
                         params={'q':'"'+args.word+'"',
                                 "tbs":"li:1"}
                        )

        soup = BeautifulSoup(r.text, "lxml")
        line= soup.find('div',{'id':'resultStats'}).text
        line=line.replace(',','')
        results=int(re.search(r'\d+', line).group())
        print ('Google Search Results: ', results)
        return log2(google_index/results)

        
        
    

#arg 1 directory arg 2 search term arg 3 number of results wanted(default is 10)
if __name__ == '__main__':
    directory=argv[1]
    search_term=argv[2]
    if len(argv)>3:
        count=argv[3]
    else:
        count=10
    search=search_dir()
    CA= corpus_analysis()
    #searches directory for matching txt files excluding hash table
    file_list=search.files_contain(directory, search_term)
    #gets the TF and IDF and TF-IDF for each file and stores it in a list
    results_list=[]
    round_to_n=lambda x, n: round(x, -int(floor(log10(abs(x))))+(n-1))
    IDF=CA.get_IDF(search_term)
    rIDF=round_to_n(IDF, 3)
    print('IDF: ', IDF)
    for filepath in file_list[:count]:
        print(filepath)
        TF=CA.get_TF(filepath, search_term)
        print('TF: ',TF)
        TF_IDF=TF * IDF
        TF=round_to_n(TF, 3)
        TF_IDF=round_to_n(TF_IDF, 3)
        URL=search.get_orig_URL( (os.path.splitext(os.path.basename(filepath))[0].rstrip() + '.html'), os.path.join(directory, 'hash_table.txt'))
        results_list.append([TF_IDF, TF, rIDF, URL])
    with open('TF_IDF_results.txt', 'w') as outresults:
        print('TF-IDF', 'TF', 'IDF', 'URL', sep='\t', end='\n', file=outresults)
        for result in results_list:
            print(*result, sep='\t', file=outresults)
        
            
        
        
