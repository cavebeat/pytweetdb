'''
Created on 23 May 2017

@author: cave

'''
#!/usr/bin/env python
# encoding: utf-8


import tweepy
import requests, re

#copy example.config.py to config.py and edit the values for your Twitter API
import config
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret


##authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Local PictShare Server
cdn = 'http://cdn.cavebeat.lan/backend.php?getimage='
tweetimageurl = ''
twlink = 'https://twitter.com/wichtigeInfos/status/' 


##http://docs.tweepy.org/en/v3.5.0/api.html#API.user_timeline
tweets = api.user_timeline("wichtigeinfos", page = 1, count = 2, tweet_mode="extended")

for tweet in tweets:
##    #print tweet.id, tweet.created_at, tweet.text.encode("utf-8"),  tweet.retweeted
    print twlink + str(tweet.id), tweet.created_at, "\n", re.sub(r"https://t.co\S+", "", tweet.full_text.encode("utf-8"))
    if 'hashtags' in tweet.entities:
        for tags in  tweet.entities['hashtags']:
            print "TAGS:", tags['text']
    if 'urls' in tweet.entities:
        #print tweet.entities
        for url in tweet.entities['urls']:
            print "URLS:", url['url']
            
            
    if 'media' in tweet.entities:
        
        for image in  tweet.entities['media']:
            #print "MEDIAURL", image['media_url']
            tweetimageurl = image['media_url']
            
            uploadurl = cdn + tweetimageurl
            r = requests.get(uploadurl)
            j = r.json()
            print "CDNURL", j["url"]
    print "\n"
    

#print uploadurl
