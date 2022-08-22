class C(object):
    def __init__(self):
        self.x = 0
        self._x = 1
        self.__x = 2

class Derived(C):
    def print_c(self):        
        base_instance = C()
        derived_instance = Derived()
        print("Access public member with base class instance: %d\n" % (base_instance.x))
        print("Access public member with derived class instance: %d\n" % (derived_instance.x))
        print("Access protected member in derived class with base class instance: %d\n" % (base_instance._x))
        print("Access protected member in derived class with derived class instance: %d\n" % (derived_instance._x)) 
        print("Cannot access private member from outsite its scope\n") # print(base_instance.__x) # print(derived_instance.__x)

Derived().print_c()

base_instance = C()
print("Access (but not advised) protected member outside its scope with base class instance: %d\n" % (base_instance._x))
derived_instance = Derived()
print("Access (but not advised) protected member outside its scope with derived class instance: %d\n" % (derived_instance._x))

