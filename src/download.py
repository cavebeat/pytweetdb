#!/usr/bin/env python
# encoding: utf-8
'''
Created on 28 May 2017

@author: cave

'''

import MySQLdb, tweepy, requests, re

import config





def cdn_upload(cdn, twitter):
    #upload media to cdn pictshare               
    uploadurl = cdn + twitter
    r = requests.get(uploadurl)
    j = r.json()
    return j



def chk_author(tw_id):
    u = api.get_user(tw_id)
    print 'UserID: ', u.id, 'UserName:', u.screen_name

    if read_user(u.id) is False:
        #ls_author = ('0id', '1author', '2img_src', '3src_hash', '4img_cdn', '5cdn_hash' )
        insert_user(u.id, u.screen_name, u.profile_image_url)
                  
#     uploadurl = cdn + twitter
#     r = requests.get(uploadurl)
#     j = r.json()
    return 1

def read_user(tw_id):
# prepare a cursor object using cursor() method
    cursor = db.cursor()
      
    sql = "SELECT * FROM author \
        WHERE id = '%d'" % tw_id
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        print results[0], results[1], results[2], results[3], results[4], results[5]
        return True
    except:
        print "Error: unable to fecth data"
        return False 


def insert_user(tw_id, tw_screen_name, tw_profile_image_url):
    
    
    

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

##authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



# Open database connection
db = MySQLdb.connect("192.168.100.201",             #Host
                     "wichtigeinfos",               #User
                     "ANLvefC8X3TB4poz9QcqS7tPk",   #Password
                     "wichtigeinfos" )              #Database


#Local PictShare Server
cdn = 'http://cdn.cavebeat.lan/backend.php?getimage='
tweetimageurl = ''
twlink = 'https://twitter.com/wichtigeInfos/status/' 

ls_tweet = ('0tw_id', '1author_id', '2text', '3link_src', '4grafik_src', '5grafik_cdn', '6date', '7time', '8tags', '9links')
ls_author = ('0id', '1author', '2img_src', '3src_hash', '4img_cdn', '5cdn_hash' )
ls_tags = ('id')
ls_links = ('id')

##http://docs.tweepy.org/en/v3.5.0/api.html#API.user_timeline
tweets = api.user_timeline("wichtigeinfos", page = 1, count = 3, tweet_mode="extended")



u = api.get_user('wichtigeinfos')
print 'UserID: ', u.id, 'UserName:', 'wichtigeInfos'






for tweet in tweets:
##    #print tweet.id, tweet.created_at, tweet.text.encode("utf-8"),  tweet.retweeted
    print twlink + str(tweet.id), tweet.created_at, "\n", re.sub(r"https://t.co\S+", "", tweet.full_text.encode("utf-8"))
    if tweet.retweeted is False:
        if 'hashtags' in tweet.entities:
            for tags in  tweet.entities['hashtags']:
                print "TAGS:", tags['text']
        if 'urls' in tweet.entities:
            #print tweet.entities
            for url in tweet.entities['urls']:
                print "URLS:", url['url']                 
        if 'media' in tweet.entities:         
            for image in  tweet.entities['media']:
                j = cdn_upload(cdn, image['media_url'])
#                 tweetimageurl = image['media_url']               
#                 uploadurl = cdn + tweetimageurl
#                 r = requests.get(uploadurl)
#                 j = r.json()
                print "CDNURL", j["url"]
        print "\n"


# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT * FROM author \
       WHERE author = 'cavebeat' "
try:
    cursor.execute(sql)
    results = cursor.fetchone()
    print results
except:
    print "Error: unable to fetch data"


# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO author (author, img_src, img_cdn) \
    VALUES ('cavebeat', 'https://pbs.twimg.com/profile_images/512934277/cave.jpg', 'http://cdn.cavebeat.lan//ph3tf63ju3.jpg')"""
    
try:
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()
    
    
    

# disconnect from server
db.close()
