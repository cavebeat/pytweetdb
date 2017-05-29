#!/usr/bin/env python
# encoding: utf-8
'''
Created on 28 May 2017
@author: cave

'''
from puddlestuff.functions import false



def cdn_upload(cdn, twitter):
    #import cdn as url prefix, twitter as external url
    #upload media to cdn pictshare               
    #concatenate the prefix and the external url
    uploadurl = cdn + twitter
    #basically curl cdn/backend.php?externalURL
    r = requests.get(uploadurl)
    j = r.json()
    #return the url of the uploaded image
    return j["url"]


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
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])

         
    if results[0] == tw_id:
        #author already exists in db
        ##print 'EXISTS: ', tw_id 
        return True
    else: 
        return False
    
    
def read_tweet(tw_id):
# prepare a cursor object using cursor() method
    cursor = db.cursor()
      
    sql = "SELECT * FROM tweets \
        WHERE tw_id = '%s'" % tw_id
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        if results[0] == tw_id:
            return True
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return False    
    
    
def read_tags(tw_id, tag):
# prepare a cursor object using cursor() method
    cursor = db.cursor()
      
    sql = "SELECT * FROM tags \
        WHERE id == '%s'" % tw_id
    try:
        cursor.execute(sql)
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        return False        

    results = cursor.fetchone()
    if results[0] == tw_id and results[1] == tag:
        return True
    else:
        return False    
    
#ls_tweet = ('0tw_id', '1author_id', '2text', '3link_src', '4grafik_src', '5grafik_cdn', '6date', '7time', '8tags', '9links')    
def insert_tweet(tweet_id, user_id, full_text, url_src, img_src, img_cdn, _date, _time):
    cursor = db.cursor()
   
    tw_id = "'" + str(tweet_id) + "'"       #123456789
    author_id = "'" + str(user_id) + "'"         #username
    text = "'" + full_text + "'"            #lorem ipsum
#     text = text.encode('utf8')
    link_src = "'" + url_src + "'"          #https://twitter.com/wichtigeInfos/status/123456789
    grafik_src = "'" + img_src + "'"        #pbs.twimg
    #grafik_src.encode("utf-8")
    grafik_cdn = "'" + img_cdn + "'"        #cdn.cavebeat.lan #pictshare
    #grafik_cdn.encode("utf-8")
    date = "'" + str(_date) + "'"
    time ="'" + str(_time) + "'"
#    grafik_src = "'" + 'asdf' + "'"        #pbs.twimg
#    grafik_cdn = "'" + 'adsf' + "'"        #cdn.cavebeat.lan #pictshare


    sql = """INSERT INTO tweets (tw_id, author_id, text, link_src, grafik_src, grafik_cdn, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""% \
    (tw_id, author_id, text, link_src, grafik_src, grafik_cdn, date, time) 
       
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        return True
    except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        # Rollback in case there is any error
        db.rollback()
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
    


import MySQLdb, tweepy, requests, re
import config
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
                     "wichtigeinfos",               #Database
                     use_unicode=True, 
                     charset="utf8")   


#Local PictShare Server
cdn = 'http://cdn.cavebeat.lan/backend.php?getimage='
tweetimageurl = ''
twlink = 'https://twitter.com/wichtigeInfos/status/' 

ls_tweet = ('0tw_id', '1author_id', '2text', '3link_src', '4grafik_src', '5grafik_cdn', '6date', '7time', '8tags', '9links')
ls_author = ('0id', '1author', '2img_src', '3img_cdn', '4cdn_hash' )
ls_tags = ('id')
ls_links = ('id')

##http://docs.tweepy.org/en/v3.5.0/api.html#API.user_timeline
tweets = api.user_timeline("wichtigeinfos", page = 1, count = 2, tweet_mode="extended")


for tweet in tweets:
    if tweet.retweeted is False:
        
        #check if author of tweet is already in the db, if not upload img and insert to db.author
        chk_author(tweet.user.id)
        #extract images of the tweet and upload to CDN
        if 'media' in tweet.entities:         
            for image in  tweet.entities['media']:
                grafik_src = image['media_url']
                grafik_cdn = cdn_upload(cdn, image['media_url'])
                print "CDNURL", grafik_cdn 
        
        print twlink + str(tweet.id), tweet.created_at, "\n", re.sub(r"https://t.co\S+", "", tweet.full_text.encode("utf-8"))
        if read_tweet(tweet.id) is False:
            insert_tweet(tweet.id, tweet.user.id, 
                         re.sub(r"https://t.co\S+", "", tweet.full_text.encode("utf-8")), 
                         twlink + str(tweet.id), 
                         grafik_src.encode("utf-8"), grafik_cdn.encode("utf-8"), tweet.created_at.date(), tweet.created_at.time())
        
        #extract the Hashtags and insert into the DB
        if 'hashtags' in tweet.entities:
            for tags in  tweet.entities['hashtags']:
                print "TAGS:", tags['text']
                if read_tags(tweet.id, tags['text']) is False:
#                     insert_tags(tweet.id, tags['text'])
                    print 'tag nicht vorhanden'
        #extract the links/URL from tweet and insert into DB
        if 'urls' in tweet.entities:
            #print tweet.entities
            for url in tweet.entities['urls']:
                print "URLS:", url['url']               
        print "\n"

# disconnect from server
db.close()






