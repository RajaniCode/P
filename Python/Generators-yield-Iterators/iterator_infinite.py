class Even(object):
    def __iter__(self):
        self.n = -2
        return self

    def next(self):
        self.n += 2
        return self.n

e = Even()
iterable = iter(e)

# Single digit even numbers
for value in iterable:
    print(value)
    if value >= 8:
        break

# Or
# The for statement iterates through a collection or iterable object or generator function
# The while statement simply loops until a condition is False.
'''
count = 0
while True:
    # Only in Python 2.7
    # n = iterable.next()
    n = next(iterable) # Note: iterable.__next__()  # is same as # next(iterable) in Python 3.5
    print(n)
    count = count + 1
    if count == 5:
        break
        
# infinite

while True:
    n = next(iterable)
    print(n)  
'''
