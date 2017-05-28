'''
Created on 28 May 2017

@author: cave

'''
#!/usr/bin/env python
# encoding: utf-8

import MySQLdb


# Open database connection
db = MySQLdb.connect("192.168.100.201",             #Host
                     "wichtigeinfos",               #User
                     "ANLvefC8X3TB4poz9QcqS7tPk",   #Password
                     "wichtigeinfos" )              #Database

# prepare a cursor object using cursor() method
cursor = db.cursor()


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

