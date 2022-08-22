from __future__ import print_function

print("alphanumeric")
dictionary = {'name': 'Foo', 10: [20, 30, 40], 50: 60, 70: 80, 0.9: 90, 2: 3, '': None, None: '', True: 10, False: 1, 1: True, 0: False}
print("dictionary retains only unique keys and undefined order despite duplicate keys and given order")
print(dictionary)
print(type(dictionary).__name__)
print(len(dictionary))
print("")

print("alphanumeric sorted Only in Python 2.7")
print("Print dictionary sorted by keys")
# iterkeys() Only in Python 2.7
for key in sorted(dictionary.keys()):
    print("%s: %s" % (key, dictionary[key]))
print("")

print("alphanumeric sorted Only in Python 2.7")
print("Print dictionary sorted by values")
# iteritems() Only in Python 2.7
for key, value in sorted(dictionary.items(), key=lambda x: x[1], reverse=False):
    print("%s: %s" % (key, value))
print("")

print("alpha")
dictionary = {'a': 'Austria', 'c': 'Canada', 'b': 'Belgium', 'A': 'Australia', 'C': 'Cuba', 'B': 'Brazil', 'A': 'Antartica'}
print("dictionary retains only unique keys and undefined order despite duplicate keys and given order")
print(dictionary)
print(type(dictionary).__name__)
print(len(dictionary))
print("")

print("Print dictionary sorted by keys")
# iterkeys() Only in Python 2.7
for key in sorted(dictionary.keys()):
    print("%s: %s" % (key, dictionary[key]))
print("")

print("Print dictionary sorted by values")
# iteritems() Only in Python 2.7
for key, value in sorted(dictionary.items(), key=lambda x: x[1], reverse=False):
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
# iterkeys() Only in Python 2.7
for key in sorted(dictionary.keys()):
    print("%s: %s" % (key, dictionary[key]))
print("")

print("Print dictionary sorted by values")
# iteritems() Only in Python 2.7
for key, value in sorted(dictionary.items(), key=lambda x: x[1], reverse=False):
     print("%s: %s" % (key, value))
