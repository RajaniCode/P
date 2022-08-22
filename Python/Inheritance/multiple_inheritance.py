from abc import ABCMeta

class A(object):    
    def method(self):
        print("Class A method")

# class Abstract(object):
# class Abstract(A):
class Abstract:
    __metaclass__ = ABCMeta
    def method(self):
        print("Class Abstract method")

Abstract.register(tuple)

assert issubclass(tuple, Abstract)
assert isinstance((), Abstract)

print(issubclass(tuple, Abstract))
print(isinstance((), Abstract))
print("Abstract is subclass of object", issubclass(Abstract, object))

class B(object):
    def method(self):
        print("Class B method")
        


class C(Abstract, A, B):
    def method(self):
        print("Class C method")

print("C is subclass of object", issubclass(C, object))    
print("C is subclass of Abstract", issubclass(C, Abstract))
print("C is subclass of A", issubclass(C, A))
print("C is subclass of B", issubclass(C, B))

# Note the following will not work for C to inherit from B, B must be defined before C
'''
class B(object):
    def method(this):
        print("Class B method")
'''

class D(C):
    def method(self):
        print("Class D method")

# class E(C, D): #Will not work
class E(D, C): 
    def method(self):
        print("Class E method")

class F(E):
    @staticmethod
    def smethod():
        print("Class F @staticmethod")

class G(F):
    @staticmethod
    def smethod():
        print("Class G @staticmethod")

class H(G, F):
    @staticmethod  
    def smethod():
        print("Class H @staticmethod")
    def method(self):
        print("Class H method")

Abstract().method()
A().method()
B().method()
C().method()
D().method()
E().method()

F().smethod()
G().smethod()
H().smethod()

H().method()

F.smethod()
G.smethod()
H.smethod()



