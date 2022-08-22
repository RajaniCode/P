import gc
import weakref

class C:
    def method(self):
        print("method called!")

c = C()
r = weakref.ref(c.method)
r()

r = weakref.WeakMethod(c.method) # Python 3.5
r() # Python 3.5
r()() # Python 3.5

del c
print(gc.collect())


'''
Python 3.5 (https://repl.it/languages/python3)
method called!
0
'''
