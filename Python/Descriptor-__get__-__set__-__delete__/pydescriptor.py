class Descriptor(object):
    def __init__(self):
        self.value = ""
    def __get__(self, obj, objtype):
        print("get")
        return self.value
    def __set__(self, obj, value):
        print("set")
        self.value = value
    def __delete__(self, obj):
        print("delete")
        del self.value

class Foo(object):
    d = Descriptor()

f = Foo()
f.d = 1
print(f.d)
del f.d
    
