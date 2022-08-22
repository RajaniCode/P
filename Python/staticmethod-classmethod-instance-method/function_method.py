class A(object):
    @staticmethod
    def static_method():
        print("self or cls is not passed")
    @classmethod
    def class_method(cls):
        print("cls (convention not keyword) is passed")
    def instance_method(self):
        print("self (convention not keyword) is passed")

print("static method")
A.static_method()
A().static_method()
print("")

print("class method")
A.class_method()
A().class_method()
print("")

print("instance method")
# A.instance_method() # Will not work
A().instance_method()
print("")

print(type(A.static_method))
print(type(A().static_method))

print(type(A.class_method))
print(type(A().class_method))

print(type(A.instance_method))
print(type(A().instance_method))

'''
Python 2.7

static method
self or cls is not passed
self or cls is not passed

class method
cls (convention not keyword) is passed
cls (convention not keyword) is passed

instance method
self (convention not keyword) is passed

<type 'function'>
<type 'function'>
<type 'instancemethod'>
<type 'instancemethod'>
<type 'instancemethod'>
<type 'instancemethod'>

Python 3 (https://repl.it/)

static method
self or cls is not passed
self or cls is not passed

class method
cls (convention not keyword) is passed
cls (convention not keyword) is passed

instance method
self (convention not keyword) is passed

<class 'function'>
<class 'function'>
<class 'method'>
<class 'method'>
<class 'function'>
<class 'method'>
'''
