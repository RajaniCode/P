def func():
    for i in range(10):
        x = yield i
        print 'got sent:', x

iterable = func()
# print(iterable.send("Hello World!")) # TypeError: can't send non-None value to a just-started generator
print(next(iterable)) # print(iterable.next()) # Python 2.7
print("")
print(iterable.send("Hello World!"))
print("")
print(next(iterable))
print("")
print(iterable.send("Hola!"))

'''for i in iterable:
    print i'''
