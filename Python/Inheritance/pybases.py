class A(object): pass

class B(A): pass

class C: pass

a = A()
print("type(a).__name__")
print(type(a).__name__)
print("")

print("isinstance(a, A)")
print(isinstance(a, A))
print("")

print("A.__bases__[0].__name__")
print(A.__bases__[0].__name__)
print("")

print("issubclass(A, object)")
print(issubclass(A, object))
print("")

print("a.__class__.__bases__[0].__name__")
print(a.__class__.__bases__[0].__name__)
print("")

print("isinstance(a, object)")
print(isinstance(a, object))
print("")

b = B()
print("type(b).__name__")
print(type(b).__name__)
print("")

print("isinstance(b, B)")
print(isinstance(b, B))
print("")

print("B.__bases__[0].__name__")
print(B.__bases__[0].__name__)
print("")

print("issubclass(B, A)")
print(issubclass(B, A))
print("")

print("b.__class__.__bases__[0].__name__")
print(b.__class__.__bases__[0].__name__)
print("")

print("isinstance(b, A)")
print(isinstance(b, A))
print("")

print("issubclass(B, object)")
print(issubclass(B, object))
print("")

print("isinstance(b, object)")
print(isinstance(b, object))
print("")


c = C()
print("type(c).__name__")
print(type(c).__name__) # instance in Python 2.7 # C in Python 3.5 
print("")

print("isinstance(c, C)")
print(isinstance(c, C))
print("")

# print(C.__bases__[0].__name__) # IndexError: tuple index out of range in Python 2.7
print("if C.__bases__: print(C.__bases__[0].__name__)")
if C.__bases__: print(C.__bases__[0].__name__)  # object in Python 3.5
print("")

print("issubclass(C, object)")
print(issubclass(C, object)) # False in Python 2.7 # True in Python 3.5
print("")

# print(c.__class__.__bases__[0])  # IndexError: tuple index out of range in Python 2.7
print("if c.__class__.__bases__: print(c.__class__.__bases__[0].__name__)")
if c.__class__.__bases__: print(c.__class__.__bases__[0].__name__) # object in Python 3.5
print("")

print("isinstance(c, object)")
print(isinstance(c, object))
print("")

'''
print("type(a).__class__.__name__")
print(type(a).__class__.__name__)
print("")

print("type(b).__class__.__name__")
print(type(b).__class__.__name__)
print("")

print("type(c).__class__.__name__")
print(type(c).__class__.__name__)
print("")
'''
