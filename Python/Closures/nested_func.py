def Outer(x):
    print("Square of %d = %d" % (x, (x ** 2)))
    def Inner(x):
        print("Cube of %d = %d" % (x, (x ** 3)))
    return Inner

out = Outer(5)
out(6)
# del Outer
o = Outer(7) # NameError: name 'Outer' is not defined
out(8)
