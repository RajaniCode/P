# legacy-style, the resolution order is D - B - A - C - A:
# so when looking up D.x,
# A is the first base in resolution order to solve it, thereby hiding the definition in C
# 'a'
# class A: x = 'a'

# new-style, the order is: D - B - C - A - object
# 'c'
class A(object): x = 'a'

class B(A): pass

class C(A): x = 'c'

class D(B, C): pass

print(D.x)

# print(D.__mro__) #
