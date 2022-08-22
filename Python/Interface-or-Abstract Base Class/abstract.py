from abc import ABCMeta

# Python 3.5
#class MyABC(metaclass=ABCMeta): pass
class MyABC(object):  
    __metaclass__ = ABCMeta #

MyABC.register(tuple)

assert issubclass(tuple, MyABC)
assert isinstance((), MyABC)

print(issubclass(tuple, MyABC))
print(isinstance((), MyABC))
