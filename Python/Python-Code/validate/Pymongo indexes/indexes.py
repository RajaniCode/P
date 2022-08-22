import sys
import pymongo


# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")


# get a handle to the school database
db = connection.blog
posts = db.posts


def create_indexes():
    try:
        print "db.posts.createIndex( { date: -1 } )"
        # posts.ensure_index([ ("date", pymongo.DESCENDING)])
        posts.create_index([ ("date", pymongo.DESCENDING)])
        
        print "db.posts.createIndex( { permalink: 1 } )"
        # posts.ensure_index([ ("permalink", pymongo.ASCENDING)])
        posts.create_index([ ("permalink", pymongo.ASCENDING)])

        print "db.posts.createIndex( { tags: 1, date: -1 } )"
        # posts.ensure_index([ ("tags", pymongo.ASCENDING),("date", pymongo.DESCENDING)])
        posts.create_index([ ("tags", pymongo.ASCENDING),("date", pymongo.DESCENDING)])
        
        print "Created Indexes"
    except:
        print "Error Creating Indexes"
        print "Unexpected error:", sys.exc_info()[0]


def drop_indexes():
    try:
        print "db.posts.dropIndex( { date: -1 } )"
        posts.drop_index([ ("date", pymongo.DESCENDING)])        

        print "db.posts.dropIndex( { permalink: 1 } )"
        posts.drop_index([ ("permalink", pymongo.ASCENDING)])
        
        print "db.posts.dropIndex( { tags: 1, date: -1 } )"
        posts.drop_index([ ("tags", pymongo.ASCENDING),("date", pymongo.DESCENDING)])
        
        print "Dropped Indexes"
    except:
        print "Error Dropping Indexes"
        print "Unexpected error:", sys.exc_info()[0]


# In case indexes exist already
drop_indexes()
create_indexes()



            


        
    
