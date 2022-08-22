

#
# Copyright (c) 2008 - 2013 10gen, Inc. <http://10gen.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import random
import string
import hashlib
import pymongo
import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the school database
db = connection.blog
users = db.users
SECRET = 'verysecret'

# makes a little salt
def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt

    # implement the function make_pw_hash(name, pw) that returns a hashed password
    # of the format:
    # HASH(pw + salt),salt
    # use sha256

def make_pw_hash(pw,salt=None):
    if salt == None:
        salt = make_salt()
    return hashlib.sha256(pw.encode('utf-8') + encode('utf-8')).hexdigest()+","+ salt

# Validates a user login. Returns user record or None
def validate_login(username, password):
    user = None
    try:
        query = {'_id':username}  
        user = users.find_one(query)
        print("user doc:\n", user)
        print("user['_id']:", user['_id'])
        print("user['password']:", user['password'])
    except:
        print("Unable to query database for user")

    if user is None:
        print("User not in database")
    return None

    salt = user['password'].split(',')[1]

    if user['password'] != make_pw_hash(password, salt):
        print("user password is not a match")
    return None

    # Looks good
    return user


# creates a new user in the users collection
def add_user(username, password, email):
    password_hash = make_pw_hash(password)

    user = {'_id': username, 'password': password_hash}
    if email != "":
        user['email'] = email
        try:
            users.insert_one(user)
            print("This space intentionally left blank.")

        except pymongo.errors.OperationFailure:
            print("oops, mongo error")
            return False
        except pymongo.errors.DuplicateKeyError as e:
            print("oops, username is already taken")
            return False

    return True

validate_login('impavid', 'spartan')



