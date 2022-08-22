''' As long as there's single inheritance, __mro__ is just the tuple of:
the class, its base, its base's base, and so on up to object
(only works for new-style classes of course)'''

# class A: pass # Will not work for legacy-style classes

# Method Resolution Order (MRO) in new style Python classes

class A(object): pass

print(A.__mro__)

class B(A): pass

print(B.__mro__)

class C(A): pass

print(C.__mro__)

class D(B, C): pass

print(D.__mro__)
