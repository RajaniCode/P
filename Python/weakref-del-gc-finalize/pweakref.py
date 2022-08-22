import weakref

class D(dict):
    pass

wr = D(red = 1, green = 2, blue = 3)
r = weakref.ref(wr)
wr2 = r()

print(wr is wr2)
print(wr2 is wr)
print("")

print(isinstance(wr, D))
print(isinstance(wr2, D))
print(isinstance(r(), D))
print("")

del wr, wr2 # "Object has been deallocated; can't frobnicate"

wr = r()

if wr is None:
    print("Object has been deallocated; can't frobnicate") #
else:
    print("Object is still live!")

    
