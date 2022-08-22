from __future__ import print_function
import collections

def generator(x):
    for i in range(len(x) -1, -1, -1):
        yield x[i]

x = "Hello World!"
# x = [1, 2, 3]

iterable = generator(x)



for value in iterable:
    print(value, end="")
print("")

iterable = generator(x)

y = ""
for i in range(len(x)):
    y += next(iterable)
print(y.strip())




print("isinstance(iterable, collections.Iterable)")
print(isinstance(iterable, collections.Iterable))

print("hasattr([1,2,3,4], '__iter__')")
print(hasattr([1,2,3,4], '__iter__'))
print("hasattr((1,2,3,4), '__iter__')")
print(hasattr((1,2,3,4), '__iter__'))
print("hasattr(u'hello', '__iter__')") # Note
print(hasattr(u'hello', '__iter__')) # False in Python 2.7, True in Python 3.5
print("hasattr(u'hello', '__getitem__')")
print(hasattr(u'hello', '__getitem__'))
print("hasattr(iterable, '__iter__')")
print(hasattr(iterable, '__iter__'))
print("hasattr(1, '__iter__')")
print(hasattr(1, '__iter__'))

it = iterable
it = u'hello'
it = True
it = 1

try:
   _ = (e for e in it)
except TypeError:
   print(it, 'is not iterable')



