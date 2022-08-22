import sys

class MyError(Exception):
    pass

def try_except(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        # Only in Python 2.7
        # except Exception, e:
        except Exception as e:
            et, ei, tb = sys.exc_info()
            raise MyError, MyError(e), tb
            # Only in Python 3.5
            # raise MyError(e).with_traceback(tb)
            # Or Exception Chaining, Only in Python 3.5
            # raise MyError(e) from e
    return wrapped

def bottom():
   1 / 0

@try_except
def middle():
   bottom()

def top():
   middle()

top()
