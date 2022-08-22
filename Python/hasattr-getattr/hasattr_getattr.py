class Example(object):
  x = 1

eg = Example()
print(hasattr(eg, 'x'))

lst = ['alpha', 'beta', 'gamma']
print(lst.index('beta'))
print(hasattr(lst, 'index'))
print(getattr(lst, 'index')('beta'))
print(object.__getattribute__(lst, 'index')('beta'))
