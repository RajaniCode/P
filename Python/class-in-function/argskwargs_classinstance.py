from __future__ import print_function

def func(*args):
   print(type(args).__name__)
   class Bindargs(object):
       foo = args[0]
       print("foo is", foo)
       def __init__(self, args):
          print("init Bindargs", args)
   return Bindargs(args) # return an instance of the class # 'Bindargs' object is not callable

func(3,)
print("")


def function(**kwargs):
   print(type(kwargs).__name__)
   class Bindkwargs(object):
       foo = kwargs["foo"]
       print("foo is", foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)
   return Bindkwargs(kwargs) # return an instance of the class # 'Bindkwargs' object is not callable

function(foo=3)
print("")


# Note
def method(*args, **kwargs):
   print(type(args))
   print(type(kwargs))
method()
