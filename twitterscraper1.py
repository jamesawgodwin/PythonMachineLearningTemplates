"""
CONVERT JSON to CSV

import csv  
import json  
  
# Open the CSV  
f = open( '/path/to/filename.csv', 'rU' )  
# Change each fieldname to the appropriate field name. I know, so difficult.  
reader = csv.DictReader( f, fieldnames = ( "fieldname0","fieldname1","fieldname2","fieldname3" ))  
# Parse the CSV into JSON  
out = json.dumps( [ row for row in reader ] )  
print "JSON parsed!"  
# Save the JSON  
f = open( '/path/to/parsed.json', 'w')  
f.write(out)  
print "JSON saved!" 

###in terminal, in proper directory, TYPE python parser.py
#spit out in terminal TYPE print out 
"""

#https://github.com/taspinar/twitterscraper
import codecs, json
import pandas as pd
with codecs.open('20181218_tumblrisdead.json', 'r', 'utf-8') as f:
    tweets = json.load(f, encoding='utf-8')
    
list_tweets = [list(elem.values()) for elem in tweets]
list_columns = list(tweets[0].keys())
df = pd.DataFrame(list_tweets, columns=list_columns) 




#masterDataFrame = [pd.read_json(f) for f in filenames]
                  
#print(tweets[10])

"""
2.3 From within Python
You can easily use TwitterScraper from within python:
====================================================
from twitterscraper import query_tweets

if __name__ == '__main__':
    list_of_tweets = query_tweets("Trump OR Clinton", 10)

    #print the retrieved tweets to the screen:
    for tweet in query_tweets("Trump OR Clinton", 10):
        print(tweet)

    #Or save the retrieved tweets to file:
    file = open(“output.txt”,”w”)
    for tweet in query_tweets("Trump OR Clinton", 10):
        file.write(tweet.encode('utf-8'))
    file.close()
===============================================================================
"""
    