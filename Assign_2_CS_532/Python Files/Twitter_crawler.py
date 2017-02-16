#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re as regex
import requests

#Variables that contains the user credentials to access Twitter API 
access_token = "826264224838057986-p2cjKY6P4qKUUbTRtDZDicIHFxXkCdu"
access_token_secret = "yTAtL6R0rb35p49qcharmzWMz5X4vQsT0Jrm2UQR7Nipf"
consumer_key = "1qH36csH37Oa1LKjgDijsxGVX"
consumer_secret = "QlVfb24OuyOGsMmF8ojWZs1N2p1eeT8ib2CK4ovntk1tpSLIaW"


#This is 
class StdOutListenerParser(StreamListener):
    
    counter=0
    
    emoticons_str = r"""(?: [:=;] [oO\-]? [D\)\]\(\]/\\OpP] )"""
    regex_str = [r'<[^>]+>', r'(?:@[\w_]+)', r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', r'(?:(?:\d+,?)+(?:\.?\d+)?)', r"(?:[a-z][a-z'\-_]+[a-z])", r'(?:[\w_]+)', r'(?:\S)' ]
        
    tokens_re = regex.compile(r'('+'|'.join(regex_str)+')', regex.VERBOSE | regex.IGNORECASE)
    emoticon_re = regex.compile(r'^'+emoticons_str+'$', regex.VERBOSE | regex.IGNORECASE)
    def tokenize(self, s):
        return self.tokens_re.findall(s)
     
    def preprocess(self, s, lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens
    def pull_uri(self, tokens):
        linklist=[]
        for i in tokens:
            if 'http' not in i:
                continue
            try:
                tpage=requests.get(i,allow_redirects=True, stream=True)
                turl=tpage.url
                if not turl.startswith('https://twitter.com') and not turl.startswith('https://t.co'):
                    linklist.append(turl)
            except Exception:
                pass
        for i in linklist:
            print (i)
            self.counter+=1
        
    def on_data(self, data):
        tweet=json.loads(data)
        if 'text' in tweet:
            tokens=self.preprocess(tweet['text'])
            self.pull_uri(tokens)
        if self.counter==2000:
            return False
        return True

    def on_error(self, status_code):
        print (status_code)
        if status_code==420:
            return False



    

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListenerParser()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['NPR http, GAGA http'])
