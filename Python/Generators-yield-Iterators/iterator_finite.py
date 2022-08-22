class NPower(object):
    def __init__(self, n, max):
        self.n = n
        self.max = max

    def __iter__(self):
        self.i = 0
        return self

    # def __next__(self): # Python 3.5
    # http://legacy.python.org/dev/peps/pep-3114/
    def next(self):
        if self.i <= self.max:
            result = pow(self.n, self.i)
            self.i += 1
            return result
        else:
            raise StopIteration


power = NPower(2, 4)
iterable = iter(power)

for value in iterable:
    print(value)

# print("\nNote: In Python 2.7 iterable.next is %s" % iterable.next)

# Or
# The for statement iterates through a collection or iterable object or generator function
# The while statement simply loops until a condition is False.
'''
count = 0
while True:
    n = next(iterable) # Note: iterable.__next__()  # is same as # next(iterable) in Python 3.5
    print(n)
    count = count + 1
    if count == 5:
        break

# Or
# raise StopIteration

while True:
    n = iterable.next()
    print(n)

'''

    
'''

# Only in Python 2.7

>>> power = NPower(2, 4)
>>> iterable = iter(power)
>>> iterable.next()
1
>>> iterable.next()
2
>>> iterable.next()
4
>>> iterable.next()
8
>>> iterable.next()
16
>>> iterable.next()

Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    iterable.next()
  File "E:\Working\Python\TODO\Python\Iterators\iterator_finite.py", line 18, in next
    raise StopIteration
StopIteration
>>>

# Python 3.5 and Python 2.7

>>> power = NPower(2, 4)
>>> iterable = iter(power)
>>> next(iterable)
1
>>> next(iterable)
2
>>> next(iterable)
4
>>> next(iterable)
8
>>> next(iterable)
16
>>> next(iterable)

Traceback (most recent call last):
  File "<pyshell#15>", line 1, in <module>
    next(iterable)
  File "E:\Working\Python\TODO\Python\Iterators\iterator_finite.py", line 18, in next
    raise StopIteration
StopIteration
>>>

'''
