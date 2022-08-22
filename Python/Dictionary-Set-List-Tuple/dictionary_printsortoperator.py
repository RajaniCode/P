from __future__ import print_function
import operator

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
