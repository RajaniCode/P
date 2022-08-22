# PyMongo find, find_one and Cursors


import pymongo
import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the school database
db = connection.blog
users = db.users


def find():

    print("find")

    query = {'_id':'impavid'}

    try:
        cursor = users.find(query)

    except Exception as e:
        print("Unexpected error:", type(e), e)

    sanity = 0
    for doc in cursor:
        print(doc)
        sanity += 1
        if (sanity > 10):
            break
        


def find_one():

    print("find one")
    query = {'_id': 'impavid'}
    
    try:
        user = users.find_one(query)
        
    except Exception as e:
        print("Unexpected error:", type(e), e)

    
    print(user)



find()
find_one()
