class C(object):
    def __init__(self):
        self.x = 0
        self._x = 1
        self.__x = 2

class Derived(C):
    def print_c(self):
        c = C()
        print("Access public member: %d\n" % (c.x))        
        print("Access protected member in derived class: %d\n" % (c._x))        
        print("Cannot access private member from outsite its scope\n") # print(c.__x)

Derived().print_c()

c = C()
print("Access (but not advised) protected member outside its scope: %d\n" % (c._x))

