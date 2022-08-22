try:
    raise ValueError
except Exception as e: #
    # Check the difference in behavior between Python 3.5 and 2.7
    raise IndexError
    # Only in Python 3.5
    # raise IndexError from e

# Python 3.5
# https://www.pythonanywhere.com/user/pluralschool/consoles/python3.5/...
'''

Python 3.5.1 (default, Dec 18 2015, 00:00:00) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> try:
...     raise ValueError
... except Exception as e:
...     raise IndexError from e
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ValueError
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
IndexError
>>>

'''

# Python 2.7
# https://www.pythonanywhere.com/user/pluralschool/consoles/python2.7/...
'''

Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> try:
...     raise ValueError
... except Exception:
...     raise IndexError
... 
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
IndexError
>>> 

'''

# Python 2 is adding custom attributes to your exception class, like:
'''class MyError(Exception):
    def __init__(self, message, cause):
        super(MyError, self).__init__(message + u', caused by ' + repr(cause))
        self.cause = cause
try:
    v = {}['a']
except KeyError as e:
    raise MyError('failed', e)'''
