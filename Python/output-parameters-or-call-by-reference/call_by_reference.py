from __future__ import print_function

def func (a, b):
    a = 'new-value' # a and b are local names
    b = b + 1 # assigned to new objects
    return a, b # return new values

x, y = 'old-value', 99
print(x, y)

x, y = func(x, y)
print(x, y)
