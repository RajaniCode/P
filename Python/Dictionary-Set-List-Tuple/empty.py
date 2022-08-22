# print('list # Non Unique')
filled = [1, 2, 3, 1]  
unfilled = []

# print('set' and 'dict')
filled = {1, 2, 3}
unfilled = {}

# print('set')
filled = set([1, 2, 3])
unfilled = set([])

# print('frozenset')
filled = frozenset([1, 2, 3])
unfilled = frozenset([])

# print('dict')
filled = {"a": "alpha", "b": "beta", "g": "gamma"}
unfilled = {}

# print('tuple # Non Unique')
filled = (1, 2, 3, 1) 
unfilled = ()

import collections
filled = {"a": "alpha", "b": "beta", "g": "gamma", "b": "delta"}
unfilled = {}
# print('collections.OrderedDict')
filled = collections.OrderedDict(filled)
unfilled = collections.OrderedDict(unfilled)

print(type(filled))
print(type(unfilled))
print("")

print(("%s is not empty" % (filled,)) if filled else ("%s is empty" % (filled,)))
print(("%s is not empty" % (unfilled,)) if unfilled else ("%s is empty" % (unfilled,)))
print("")

def is_empty(x):
    if x:
        print("%s is not empty" % (x,))        
    else:
        print("%s is empty" % (x,))

is_empty(filled)
is_empty(unfilled)
print("")

def check_length(x):
    if len(x) > 0:
        print("%s is not empty" % (x,))        
    else:
        print("%s is empty" % (x,))
        
check_length(filled)
check_length(unfilled)


# Note: "," for tuple
'''
>>> thetuple = (1, 2, 3)
>>> print "this is a tuple: %s" % (thetuple,)
this is a tuple: (1, 2, 3)
'''


# Note: "str" for tuple
'''
>>> s = "Tuple: " + str(tup)
>>> s
"Tuple: (2, 'a', 5)"
'''
