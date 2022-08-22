# http://python-reference.readthedocs.io/en/latest/docs/dunderdsc/set.html
# this is our descriptor object
class Bar(object):
    def __init__(self):
        self.value = ''
    def __get__(self, instance, owner):
        print("returned from descriptor object")
        return self.value
    def __set__(self, instance, value):
        print("set in descriptor object")
        self.value = value
    def __delete__(self, instance):
        print("deleted in descriptor object")
        del self.value

class Foo(object):
    bar = Bar()

f = Foo()
f.bar = 1
print(f.bar)
del f.bar
