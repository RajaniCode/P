import weakref

s1 = {1, 2, 3}
s2 = s1 # 1 s1 and s2 are aliases referring to the same set, {1, 2, 3}.

def bye(): # 2 This function must not be a bound method the object about to be destroyed or otherwise hold a reference to it.
    print("Gone with the wind!")

ender = weakref.finalize(s1, bye) # 3 Register the bye callback on the object referred by s1.
print(ender.alive) # 4 The .alive attribute is True before the finalize object is called.
del s1
print(ender.alive) # 5 As discussed, del does not delete an object, just a reference to it.
s2 = "spam" # Gone with the wind! # 6 Rebinding the last reference, s2, makes {1, 2, 3} unreachable. It is destroyed, the bye callback is invoked and ender.alive becomes False.
print(ender.alive)
