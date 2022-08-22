import random
import string
import hashlib

def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt

def make_pw_hash(pw,salt=None):
    if salt == None:
        salt = make_salt()
    return hashlib.sha256(pw.encode('utf-8') + salt.encode('utf-8')).hexdigest()+","+ salt

print(make_pw_hash("qwerty"))
