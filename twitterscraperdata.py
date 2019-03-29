"""

import pandas as pd
from glob import glob

filenames = glob('*.json')

masterDataFrame = [pd.read_json(f) for f in filenames]

"""
from twitterscraper import query_tweets
import json

if __name__ == '__main__':
    queries = ["tumblr AND tumblrisdead"]
    list_of_tweets = []
    
    for query in queries:
        for tweets in query_tweets(query):
            temp = {
                    #"id": tweets.id.encode('ascii', 'ignore').decode('ascii'),
                    "id": str(tweets.id),
                    #"user": tweets.user.encode('ascii', 'ignore').decode('ascii'),
                    "user": str(tweets.user),
                    #"fullname": tweets.fullname.encode('ascii', 'ignore').decode('ascii'),
                    "fullname": str(tweets.fullname),
                    #"text": str(tweets.text.encode('utf-8')),
                    "text": str(tweets.text),
                    #"url": tweets.url.encode('ascii', 'ignore').decode('ascii'),
                    "url": str(tweets.url),
                    "timestamp": str(tweets.timestamp),
                    "replies": tweets.replies,
                    "retweets": tweets.retweets,
                    "likes": tweets.likes,
                    "html": tweets.html.encode('ascii', 'ignore').decode('ascii')
                    }
            list_of_tweets.append(temp)

    print(json.dumps(list_of_tweets))
    #Or save the retrieved tweets to file:
    file = open('C:/Users/jagth/testdata.json','w+')
    #for tweet in list_of_tweets:
    file.write(json.dumps(list_of_tweets))
    file.close()