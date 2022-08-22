from __future__ import print_function

def func(**kwargs):
   class Bindkwargs(object):
       foo = kwargs['foo']
       print('foo is ', foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)
   return Bindkwargs(kwargs) # return an instance of the class # 'Bindkwargs' object is not callable

func(foo=3)

