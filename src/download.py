#!/usr/bin/env python
# encoding: utf-8
'''
Created on 28 May 2017
@author: cave

'''

import MySQLdb, tweepy, requests, re
import config
from dns.name import empty
from _mysql import NULL





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
        #ls_author = ('0id', '1author', '2img_src', '3img_cdn', '4cdn_hash' )
        insert_user(u.id, u.screen_name, u.profile_image_url_https)
    return 1

def read_user(tw_id):
# prepare a cursor object using cursor() method
    cursor = db.cursor()
      
    sql = "SELECT * FROM author \
        WHERE id = '%d'" % tw_id
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
    except:
        print "Error: unable to fetch data"

         
    if results[0] == tw_id:
        print 'EXISTS: ', tw_id 
        return True
    else: 
        return False


def insert_user(tw_id, tw_screen_name, tw_profile_image_url):
    denormal = tw_profile_image_url.replace('_normal', '')
    uploadurl = cdn + denormal
    r = requests.get(uploadurl) 
    j = r.json()
    #print "CDNURL", j["url"], j["hash"]
    
    cursor = db.cursor()
   
    author_id = "'" + str(tw_id) + "'" 
    user_id = "'" + tw_screen_name + "'"
    img_src = "'" + denormal + "'"
    img_cdn = "'" + j["url"] + "'"
    cdn_hash = "'" + j["hash"] + "'"

    sql = """INSERT INTO author (id, author, img_src, img_cdn, cdn_hash) VALUES (%s, %s, %s, %s, %s)"""% \
    (author_id, user_id, img_src, img_cdn, cdn_hash) 
       
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        # Rollback in case there is any error
        db.rollback()

    return (j["url"], j["hash"])
    
    

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
ls_author = ('0id', '1author', '2img_src', '3img_cdn', '4cdn_hash' )
ls_tags = ('id')
ls_links = ('id')

##http://docs.tweepy.org/en/v3.5.0/api.html#API.user_timeline
tweets = api.user_timeline("wichtigeinfos", page = 1, count = 3, tweet_mode="extended")


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
        chk_author(tweet.user.id)
        if 'media' in tweet.entities:         
            for image in  tweet.entities['media']:
                j = cdn_upload(cdn, image['media_url'])
#                 tweetimageurl = image['media_url']               
#                 uploadurl = cdn + tweetimageurl
#                 r = requests.get(uploadurl)
#                 j = r.json()
                print "CDNURL", j["url"]
        print "\n"





# 
# # prepare a cursor object using cursor() method
# cursor = db.cursor()
# 
# sql = "SELECT * FROM author \
#        WHERE author = 'cavebeat' "
# try:
#     cursor.execute(sql)
#     results = cursor.fetchone()
#     print results
# except:
#     print "Error: unable to fetch data"


# # Prepare SQL query to INSERT a record into the database.
# sql = """INSERT INTO author (author, img_src, img_cdn) \
#     VALUES ('cavebeat', 'https://pbs.twimg.com/profile_images/512934277/cave.jpg', 'http://cdn.cavebeat.lan//ph3tf63ju3.jpg')"""
#     
# try:
#     # Execute the SQL command
#     cursor.execute(sql)
#     # Commit your changes in the database
#     db.commit()
# except:
#     # Rollback in case there is any error
#     db.rollback()
    
    
    

# disconnect from server
db.close()
