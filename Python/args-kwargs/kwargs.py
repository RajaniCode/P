from __future__ import print_function

def func(**kwargs):
    print(type(kwargs).__name__)
    print(kwargs)

# **kwargs is always named arguments (unlike *args) and dictionary
d = {'alpha': 1, 'beta': 2, 'gamma': 3}
# func(d)

# **kwargs is always named arguments (unlike *args) and dictionary elements
func(d=1)
print("")
func(d1=1, d2=2)
print("")

# **kwargs is always named arguments (unlike *args) and dictionary of dictionaries 
func(a={'alpha': 1, 'beta': 2, 'gamma': 3})
print("")
func(n = {1: 'alpha', 2: 'beta', 3: 'gamma'})
print("")
func(a={'alpha': 1, 'beta': 2, 'gamma': 3}, n = {1: 'alpha', 2: 'beta', 3: 'gamma'})
print("")


