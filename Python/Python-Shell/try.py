import sys

try:
    fn(*args, **kwargs)
except Exception, e:
   et, ei, tb = sys.exc_info()
   print(et, ei, tb)
