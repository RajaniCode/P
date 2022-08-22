import warnings

def f():
    print 'before'
    warnings.warn('you are warned!')
    print 'after'

f()


'''

Git Bash

MINGW64 /e/Working/Python/TODO/Python/warnings
$ python ignore_warnings.py
before
after
warnings_ignore.py:5: UserWarning: you are warned!
  warnings.warn('you are warned!')

MINGW64 /e/Working/Python/TODO/Python/warnings
$ python -W ignore ignore_warnings.py
before
after

'''
