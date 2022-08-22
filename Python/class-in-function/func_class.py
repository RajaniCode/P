def func():
    x = 3
    class FuncClass(object):
        y = x
    return FuncClass

f = func()
print(callable(f))
print(f.y)
print(f().y)
print("")

def function():
    x = 3
    class FunctionClass(object):
        y = x
    return FunctionClass()

f = function()
print(callable(f))
print(f.y)
# print(f().y)
