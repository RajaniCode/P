class A(object):
    pass

class B(A):
    pass

a = A()
b = B()

print(b is a)
print(a is b)
print("")

print(isinstance(a, A))
print(isinstance(b, A))
print("")

print(isinstance(a, B))
print(isinstance(b, B))
print("")
