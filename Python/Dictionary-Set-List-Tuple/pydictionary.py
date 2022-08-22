from __future__ import print_function
import operator

dictionary = { 1: 'alpha', 2: 'beta', 3: 'gamma', 4: 'delta', 5: 'epsilon',
               2: 'beta', 6: 'zeta', 7: 'gamma', 9: None, 10: 'iota',
               None: 'kappa', 11: 'lambda', None: None, 12: 'mu', 13: 'nu' }

print("type(dictionary).__name__")
print(type(dictionary).__name__)
print(dictionary)
print(len(dictionary))
print("")

print("add if key does not exist else update # 8: 'theta'")
dictionary[8] = 'theta'
print(dictionary)
print(len(dictionary))
print("dictionary.get(8)")
print (dictionary.get(8))
print("")

print("update if key exists else add # 7: 'eta'")
dictionary[7] = 'eta'
print(dictionary)
print(len(dictionary))
print("dictionary.get(7)")
print (dictionary.get(7))
print("")

print("pop item based on key only # 9: None")
dictionary.pop(9)
print(dictionary)
print("")

print("pop item based on key only # KeyError: 20")
# dictionary.pop(20)
print(dictionary)
print("")

print("del item item based on key only # 11: 'lambda'")
del dictionary[11]
print(dictionary)
print(len(dictionary))
print("dictionary.get(11)")
print (dictionary.get(11))
print("")

print("del item item based on key only # KeyError: 20")
# del dictionary[20]
print(dictionary)
print(len(dictionary))
print("dictionary.get(None)")
print (dictionary.get(None))
print("")

print("popitem - arbitrary")
dictionary.popitem()
print(dictionary)
print(len(dictionary))
print("")

print("add if key does not exist else update")
print("dictionary[None] = None")
dictionary[None] = None
print(dictionary)
print(len(dictionary))
print("dictionary.get(None)")
print (dictionary.get(None))
print("")

print("clear")
dictionary.clear()
print(dictionary)
print(len(dictionary))
print("")

print("del dictionary")
del dictionary
print("")

l1 = ['A', 'B', 'C', 'D', 'E']
l2 = [1, 2, 3, 4, 5]
l3 = ['alpha', 'beta', 'gamma', 'delta', 'epsilon']
dictionary = { 1:l1, 2:l2, 3:l3 }
print(dictionary)
print(len(dictionary))
print("")

print("dictionary from list of tuples")
lst = [(1, 'Mango'), (2, 'Banana')]
print(type((1, 'Mango')).__name__)
print(type((2, 'Banana')).__name__)
print(type(lst).__name__)
print(lst)
dictionary = dict(lst)
print(type(dictionary).__name__)
print(dictionary)
print("")

print("dict")
dictionary = dict({1:'English', 2:'French'})
print(type(dictionary).__name__)
print(dictionary)
print("")

dictionary = {1: 'Red', 2: 'Green', 3: 'Blue'}

# print("iteritems() only in Python 2.7")
# print("for item in dictionary.iteritems(): print(item)")
# for item in dictionary.iteritems(): print(item)
# print("")

# print("iteritems() only in Python 2.7")
# from __future__ import print_function
# print("for key, value in dictionary.iteritems(): print(key, value)")
# for key, value in dictionary.iteritems(): print(key, value)
# print("")

print("for item in dictionary.items(): print(item)")
for item in dictionary.items(): print(item)
print("")

# from __future__ import print_function
print("for key, value in dictionary.items(): print(key, value)")
for key, value in dictionary.items(): print(key, value)
print("")

# from __future__ import print_function
print("for key in dictionary: print(key, dictionary.get(key))")
for key in dictionary: print(key, dictionary.get(key))
print("")

# from __future__ import print_function
print("for key in dictionary: print(key, dictionary[key])")
for key in dictionary: print(key, dictionary[key])
print("")

dictionary = {'name': 'Foo', 'number': 1 }

print("Only in Python 2.7 # dictionary.has_key('number')")
# print(dictionary.has_key('number'))
# print("")

print("'technology' in dictionary")
print('technology' in dictionary)
print("")

print("'technology' not in dictionary")
print('technology' not in dictionary)
print("")

print("dictionary['technology'] # KeyError: 'technology'")
# print(dictionary['technology'])

print("dictionary.get('technology')")
print(dictionary.get('technology'))
print("")

print("set default if key does not exist # 'Foo'")
print("dictionary.setdefault('name', 'Python')")
print(dictionary.setdefault('name', 'Python'))
print(dictionary)
print("")

print("set default if key does not exist # 'Python'")
print("dictionary.setdefault('technology', 'Python')")
print(dictionary.setdefault('technology', 'Python'))
print(dictionary) 
print("")

print("get default if key does not exist # 'Foo'")
print("dictionary.get('name', 'Python')")
print(dictionary.get('name', 'Python'))
print(dictionary) 
print("")

print("get default if key does not exist # 3.5")
print("dictionary.get('version', 3.5)")
print(dictionary.get('version', 3.5))
print(dictionary) 
print("")

print("comprehension")
print("dictionary = {x: x*x for x in range(6)}")
dictionary = {x: x*x for x in range(6)}
print(type(dictionary).__name__)
print(dictionary)
print(len(dictionary))
print("")

print("alphanumeric")
print("# sorted # Only in Python 2.7 # Python 3.5: TypeError: unorderable types: int() < str()")
dictionary = {'name': 'Foo', 10: [20, 30, 40], 50: 60, 70: 80, 0.9: 90, 2: 3, '': None, None: '', True: 10, False: 1, 1: True, 0: False}
print("dictionary retains only unique keys and undefined order despite duplicate keys and given order")
print(dictionary)
print(type(dictionary).__name__)
print(len(dictionary))
print("")

print("alpha")
dictionary = {'a': 'Austria', 'c': 'Canada', 'b': 'Belgium', 'A': 'Australia', 'C': 'Cuba', 'B': 'Brazil', 'A': 'Antartica'}
print("dictionary retains only unique keys and undefined order despite duplicate keys and given order")
print(dictionary)
print(type(dictionary).__name__)
print(len(dictionary))
print("")

print("Print dictionary sorted by keys")
for key, value in sorted(dictionary.items(), key=operator.itemgetter(0)):
    print("%s: %s" % (key, value))
print("")

print("Print dictionary sorted by values")
for key, value in sorted(dictionary.items(), key=operator.itemgetter(1)):
     print("%s: %s" % (key, value))
print("")

print("numeric")
dictionary = {1: 1, 3: 9, -5: 25, 7: 49, -0.0: .1, 9: 81, -.8: -.7, 0: 0, 0: -0, 9: 9}
print("dictionary retains only unique keys and undefined order despite duplicate keys and given order")
print(dictionary)
print(type(dictionary).__name__)
print(len(dictionary))
print("")

print("Print dictionary sorted by keys")
for key, value in sorted(dictionary.items(), key=operator.itemgetter(0)):
    print("%s: %s" % (key, value))
print("")

print("Print dictionary sorted by values")
for key, value in sorted(dictionary.items(), key=operator.itemgetter(1)):
     print("%s: %s" % (key, value))
print("")

print("dictionary not intended for get by value")
dictionary = {'a': 'Austria', 'c': 'Canada', 'b': 'Belgium', 'A': 'Australia', 'C': 'Cuba', 'B': 'Brazil', 'A': 'Antartica'}
for key, value in dictionary.items():
    if value == "Antartica": print(key, value)
