import requests
import re
from sys import argv
from urllib.parse import urljoin
from datetime import datetime
import json


class get_mementos():
  
    def get_aggregate(self, uri):
        aggregate='http://memgator.cs.odu.edu/timemap/link/'.rstrip()
        uri=aggregate+uri.rstrip()
        tbody=requests.get(uri)
        print(tbody.status_code)
        if not(tbody.status_code == 200):
                raise StopIteration
        for line in tbody:
                yield line
        
    def get_age(self, uri):
        agelink='http://localhost:8888/cd?url='.rstrip()
        uri=agelink+uri.rstrip()
        r=requests.get(uri)
        data=json.loads(r.text)
        date_string=data['Estimated Creation Date']
        try:
            cdate=datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        except:
            return "NA"
        return (datetime.now()-cdate).days
        
    def get_data(self, uri):
        num_mementos=0
        age=0
        for line in self.get_aggregate(uri):
            if b'memento' in line:
                num_mementos+=1
                    
        if num_mementos>0:
            age=self.get_age(uri)
            return(num_mementos, age)
        return (num_mementos, 'NA')



if __name__ == '__main__':
    filename=argv[1]
    r=get_mementos()
    with open("data_set.txt", 'w') as outfile:    
        with open(filename, 'r') as file:
            for line in file:
                #print(line)
                print('\t'.join(str(v) for v in r.get_data(line)), file=outfile)
