# from pymodule import *
from pymodule import Alpha

a = Alpha()

print("import static method")
Alpha.static_method()
a.static_method()
print("")

print("import class method")
Alpha.class_method()
a.class_method()
print("")

print("import instance method")
# Alpha.instance_method() # Will not work
a.instance_method()
