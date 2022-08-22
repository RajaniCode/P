import copy

a = [1, 2, 3]
b = [4, 5, 6]
c = [a, b]

# Using normal assignment operatings to copy:

d = c

print id(c) == id(d)          # True - d is the same object as c
print id(c[0]) == id(d[0])    # True - d[0] is the same object as c[0]

# Using a shallow copy:

e = copy.copy(c)

print id(c) == id(e)          # False - d is now a new object
print id(c[0]) == id(e[0])    # True - d[0] is the same object as c[0]

# Using a deep copy:

f = copy.deepcopy(c)

print id(c) == id(f)          # False - d is now a new object
print id(c[0]) == id(f[0])    # False - d[0] is now a new object
