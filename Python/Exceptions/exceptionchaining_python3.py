try:
    {}['a']
except KeyError as ke:
    # Only in Python 3.5
    raise ValueError("Error") from ke

#  Python 2.7
'''class CustomError(Exception):
    def __init__(self, message, cause):
        super(CustomError, self).__init__(message + u', caused by '+ repr(cause))
        self.cause = cause
try:
    {}['a']
except KeyError as ke:
    raise CustomError("Error", ke)'''

# Python 3.5
# https://www.pythonanywhere.com/user/pluralschool/consoles/python3.5/...
'''

Python 3.5.1 (default, Dec 18 2015, 00:00:00) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> try:
...     {}['a']
... except KeyError as ke:
...     # Only in Python 3.5
...     raise ValueError("Error") from ke
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
KeyError: 'a'
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
ValueError: Error
>>>

'''
