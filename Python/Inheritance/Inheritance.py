class BaseClass(object):
    def __new__(cls):
        # obj = super().__new__(cls) # Only in Python 3.5 # Don't Repeat Yourself
        obj = super(BaseClass, cls).__new__(cls)
        print("new BaseClass")
        return obj
    def __init__(self):
        # super().__init__() # Python 3.5
        super(BaseClass, self).__init__() # Only in Python 3.5 # Don't Repeat Yourself
        print("init BaseClass")

class DerivedClass(BaseClass):
    def __new__(cls):
        # obj = super().__new__(cls) # Only in Python 3.5 # Don't Repeat Yourself
        obj = super(DerivedClass, cls).__new__(cls)
        print("new DerivedClass")
        return obj
    def __init__(self):
        # super().__init__() # Only in Python 3.5 # Don't Repeat Yourself
        super(DerivedClass, self).__init__()
        print("init DerivedClass")

bc = BaseClass()
print("")
dc = DerivedClass()

#Note
#__new__(cls, *args, **kwargs)
#__init__(self, *args, **kwargs)

