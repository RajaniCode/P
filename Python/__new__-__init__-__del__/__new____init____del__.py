class A(object):
    def __new__(cls):
        #obj = object.__new__(cls)
        obj = super(A, cls).__new__(cls)
        # obj = super().__new__(cls) # Python 3.5
        print("new")
        return obj
        
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")
        
    @staticmethod
    def static_method():
        print("static metthod")

    @classmethod
    def class_method(cls):
        print("class metthod")

    def instance_method(self):
        print("instance metthod")

 
A.static_method()
a = A()
a.static_method()
print("")

A.class_method()
a.class_method()
print("")    

a.instance_method()
print("")

print("Note 1")
A()
print("Note 2")
b = a
print(isinstance(b, A))
print("Note 3") 
b = A()
