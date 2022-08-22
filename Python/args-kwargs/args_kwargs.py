from __future__ import print_function

def example(*args, **kwargs):    
    print(type(args).__name__)
    print(args)
    print(type(kwargs).__name__)
    print(kwargs)    
example("Hello", " ", w = "World", ex = "!")
print("")

def arg(*args):    
    for count, item in enumerate(args):
        print("%d - %s" % (count, item))        
arg('alpha', 'beta', 'gamma')
print("")

def kwarg(**kwargs):    
    for key, value in kwargs.items():
        print("%s = %s" % (key, value))
kwarg(a = 'alpha', g = 'gamma', b = 'beta')
print("")

kwarg(d = {'a': 'alpha', 'g': 'gamma', 'b': 'beta',})

def function(*args, **kwargs):
    print(type(args).__name__)
    print(args)
    print(type(kwargs).__name__)
    print(kwargs)

# Note Ruby difference
function("Hello", " ", h = "World", e = "!") 
