from __future__ import print_function

def func(**kwargs):
   class Bindkwargs(object):
       foo = kwargs['foo']
       print('foo is', foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)          
   return Bindkwargs # 'Bindkwargs' object is callable

f = func(foo=3)
f(kwargs="bar") #
f(None) #
f("") #
f(1) #
f(True) #
