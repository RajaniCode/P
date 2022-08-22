import sys

class Example(object):
    def getattribute(self, item):
        self.dict  = { "A": "Alpha", "B": "Beta", "G": "Gamma"}
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            pass  # fallback to dict
        try:
            return self.dict[item]
        except KeyError as ke:
            # raise AttributeError("The object doesn't have such attribute")
            raise AttributeError("The object doesn't have such attribute"), None, sys.exc_info()[2]#
            # Only in Python 3.5
            # raise AttributeError("The object doesn't have such attribute") from None
            # raise AttributeError("The object doesn't have such attribute") from ke
            # raise AttributeError("The object doesn't have such attribute").with_traceback(sys.exc_info()[2])
        # except Exception as ex:
            # raise AttributeError("The object doesn't have such attribute") from ex
            # raise AttributeError("The object doesn't have such attribute").with_traceback(sys.exc_info()[2])
            

eg = Example()
print(eg.getattribute('A'))
print(eg.getattribute('B'))
print(eg.getattribute('C'))


# https://www.pythonanywhere.com/user/pluralschool/files/home/pluralschool/p.py?edit
# raise AttributeError("The object doesn't have such attribute") from ex
'''
Alpha
Beta
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 12, in getattribute
    return self.dict[item]
KeyError: 'C'
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 21, in <module>
    print(eg.getattribute('C'))
  File "/home/pluralschool/p.py", line 16, in getattribute
    raise AttributeError("The object doesn't have such attribute") from ex
AttributeError: The object doesn't have such attribute
>>>
'''


# raise AttributeError("The object doesn't have such attribute") from ke
'''
Alpha
Beta
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 12, in getattribute
    return self.dict[item]
KeyError: 'C'
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 21, in <module>
    print(eg.getattribute('C'))
  File "/home/pluralschool/p.py", line 16, in getattribute
    raise AttributeError("The object doesn't have such attribute") from ke
AttributeError: The object doesn't have such attribute
>>> 
'''


# raise AttributeError("The object doesn't have such attribute") from None
'''
Alpha
Beta
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 18, in <module>
    print(eg.getattribute('C'))
  File "/home/pluralschool/p.py", line 13, in getattribute
    raise AttributeError("The object doesn't have such attribute") from None
AttributeError: The object doesn't have such attribute
>>> 
'''


# raise AttributeError("The object doesn't have such attribute") #
'''
Alpha
Beta
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 9, in getattribute
    return self.dict[item]
KeyError: 'C'
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "/home/pluralschool/p.py", line 18, in <module>
    print(eg.getattribute('C'))
  File "/home/pluralschool/p.py", line 13, in getattribute
    raise AttributeError("The object doesn't have such attribute")
AttributeError: The object doesn't have such attribute
>>>
'''
