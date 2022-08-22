from __future__ import print_function

def func(*args):
   print(type(args).__name__)
   class Bindargs(object):
       foo = args[0]
       print("foo is", foo)
       def __init__(self, args):
          print("init Bindargs", args)
   return Bindargs # 'Bindargs' object is callable

f = func(3,)
f(args="bar") #
f(None) #
f("") #
f(1) #
f(True) #
print("")


def function(**kwargs):
   print(type(kwargs).__name__)
   class Bindkwargs(object):
       foo = kwargs["foo"]
       print("foo is", foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)
   return Bindkwargs # 'Bindkwargs' object is callable

f = function(foo=3)
f(kwargs="bar") #
f(None) #
f("") #
f(1) #
f(True) #
print("")


# Note
def method(*args, **kwargs):
   print(type(args))
   print(type(kwargs))
method()
