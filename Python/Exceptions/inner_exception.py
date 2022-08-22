import sys

class CustomError(Exception): pass

try:
    raise TypeError("Test")
except TypeError as te:
    raise(CustomError(str(te)), None, sys.exc_info()[2])
    # raise(CustomError(*te.args), None, sys.exc_info()[2])


'''

Python 3.5
https://www.pythonanywhere.com/user/pluralschool/consoles/python3.5/3130055/

>>> import sys
>>> class CustomError(Exception): pass
... 
>>> try:
...     raise TypeError("Test")
... except TypeError as te:
...     raise(CustomError(str(te)), None, sys.exc_info()[2])
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: Test
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
TypeError: exceptions must derive from BaseException

'''
