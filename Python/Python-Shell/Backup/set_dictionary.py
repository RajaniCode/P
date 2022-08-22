from collections import defaultdict

d = {'foo': 123, 'bar': 456}
# print(d['baz']) # KeyError: 'baz'

d = defaultdict(lambda: -1, d)
print(d['baz'])
-1


s = {1,2,4,5,6}
t = {}

u = t.fromkeys(s, 0)
print(u)

v = dict.fromkeys(s, 0)
print(v)

w = {}.fromkeys(s, 0)
print(w)

x = {e:0 for e in s} # https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions
print(x)


# Most Pythonic Way to Build Dictionary From Single List

lis = ['a', 'b', 'c', 'd']
dic = {x: 0 for x in lis}
print(dic)

# For 2.6 and earlier:
dic = dict((x, 0) for x in lis)
print(dic)

# timeit comparisons:

# import timeit
# print(timeit.timeit, dict.fromkeys(xrange(10000), 0))
# OR
# >> import timeit
# >> timeit.timeit, dict.fromkeys(xrange(10000), 0)
# 1000 loops, best of 3: 1.4 ms per loop

# print(timeit.timeit, {x: 0 for x in xrange(10000)})
# OR
# >> import timeit
# >> timeit.timeit, {x: 0 for x in xrange(10000)}
# 100 loops, best of 3: 2.08 ms per loop

# print(timeit.timeit, dict((x, 0) for x in xrange(10000)))
# OR
# >> import timeit
# >> timeit.timeit, dict((x, 0) for x in xrange(10000))
# 100 loops, best of 3: 4.63 ms per loop

# note that fromkeys() and dict-comprehensions may return different objects if the values used are mutable objects:
dic = dict.fromkeys(lis, [])
print(dic)

dic = [id(x) for x in dic.values()] # all point to a same object
print(dic)

dic = {x: [] for x in lis}
print(dic)

dic = [id(x) for x in dic.values()] # unique objects
print(dic)

# Default

zebra = {'Name': 'Zebra', 'Age': 7}

print(zebra.setdefault('Age', None))
print(zebra.setdefault('Speed', None))

horse = {'Name': 'Horse', 'Age': 10}

print(horse.get('Age'))
print(horse.get('Speed', "Unknown"))
