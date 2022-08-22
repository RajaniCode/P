# __call__
print("__call__")
class Foo:
  def __call__(self):
    print("called")

foo_instance = Foo()
foo_instance() #this is calling the __call__ method

class Add:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        print("Sum of", self.num1,"and",self.num2, "is:")
     
    def __call__(self):
        return (self.num1 + self.num2)

def func():
   print("func is callable, func() is not callable")

a = Add(1,2)
print(a())
x = 1
f = func()

print(callable(a)) # True
print(callable(Add)) # True
print(callable(x)) # False
print(callable(func)) # True
print(callable(func())) # False
print(callable(f)) # False
print("\n")


# __getattr__-__getattribute__
print("__getattr__-__getattribute__")
class Dictionary(object):
    def __init__(self):
        self.x = 1
        self.y = 2
    # def __getattr__(self, name):
    def __getattribute__(self, name): #
        if name == 'x':
            return 0
        else:
            return object.__getattribute__(self, name)

d = Dictionary()

print(d.x)
print(d.y)
print("\n")


# __getitem__-__setitem__-__delitem__
print("__getitem__-__setitem__-__delitem__")
class Colors(object):
    def __init__(self):
        self.data = {"Red": 1, "Green": 2, "Blue": 3}
    def __getitem__(self, item):
        print("getitem")
        return self.data[item]
    def __setitem__(self, item, value):
        print("setitem")
        self.data[item] = value
    def __delitem__(self, item):
        print("delitem")
        del self.data[item]

rgb = Colors()
print(rgb["Red"])
rgb["Blue"] = 300
print(rgb["Blue"])
print(rgb["Green"])
del rgb["Green"]
print("\n")


# __main__
print(__name__)
if __name__ == "__main__":
    print('This program is being run by itself')
else:
    print('I am being imported from another module')

print("\n")


# __new__-__init__-__del__
print("__new__-__init__-__del__")
class A(object):
    def __new__(cls):
        #obj = object.__new__(cls)
        # obj = super(A, cls).__new__(cls)
        obj = super().__new__(cls) # Python 3.5
        print("new")
        return obj
        
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")
        
    @staticmethod
    def static_method():
        print("static metthod")

    @classmethod
    def class_method(cls):
        print("class metthod")

    def instance_method(self):
        print("instance metthod")
 
A.static_method()
a = A()
a.static_method()
A.class_method()
a.class_method()
a.instance_method()
print("Note 1")
A()
print("Note 2")
b = a
print(isinstance(b, A))
print("Note 3") 
b = A()
print("\n")


# restrict new
print("restrict new")
class Restricted(object):
    MAX_Instance = 4
    CLS_Instance = 0
    def __new__(cls):
        if(cls.CLS_Instance >= cls.MAX_Instance):
            raise ValueError("Cannot create more objects")
        cls.CLS_Instance += 1
        return object.__new__(cls)

a = Restricted()
b = Restricted()
c = Restricted()
d = Restricted()
# e = Restricted()
print("\n")


# __str____repr__
print("__str____repr__")
import gc

class Node: # class Node(object):
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def addchild(self, node):
        self.parent = self
        self.children.append(node)

    def __repr__(self):
        return "<Node %s at %x>" % (repr(self.name), id(self))
    
    def __str__(self): # __str__ overrides __repr__
        return self.name
            
root = Node("Alpha")
print(root)
root.addchild(Node("Beta"))
root.addchild(Node("Gamma"))
root.addchild(Node("Delta"))
del root
print(gc.collect(), "unreachable objects")
print(gc.collect(), "unreachable objects")        
print("\n")


# all any
print("all any")

x = [-5, -4, -3, -2, -1, 0]
x = [-5, -4, -3, -2, -1]
print("print(all(i < 0 for i in [-5, -4, -3, -2, -1]))")
print(all(i < 0 for i in x))
print()

x = [0, 1, 2, 3, 4, 5]
x = [-1, 0, 1, 2, 3, 4, 5]
print("print(all(i < 0 for i in [-1, 0, 1, 2, 3, 4, 5]))")
print(any(i < 0 for i in x))
print()

print("all(l == 't' for l in 'python')")
print(all(l == 't' for l in 'python'))
print()

print("any(l == 't' for l in 'python')")
print(any(l == 't' for l in 'python'))
print()

g = (l == 't' for l in 'python')
any(g)
any( (l == 't' for l in 'python') ) # same as any(g)

print("generator = (l == 't' for l in 'python') next()")
generator = (l == 't' for l in 'python')
# .next() Only in Python 2.7
print(next(generator)) # False. 'p' is not equal to 't'
print(next(generator)) # False. 'y' is not equal to 't'
print(next(generator)) # True. 't' is equal to 't'
print()

print("generator = (l == 't' for l in 'python')")
generator = (l == 't' for l in 'python')
for value in generator:
    print(value)
print()

def t():
    print('In True!')
    return True

def f():
    print('In False!')
    return False

# Store functions to be called in a list
funcs = [t, f, f, f, t]

def test_all():
    # Pass a generator expression with function calls to all
    print(all(func() for func in funcs))
test_all() # Calls t() then f() and then stops

def test_any():
    # Pass a generator expression with function calls to any
    print(any(func() for func in funcs))
test_any() # Calls t() once and stops.
print("\n")


# *args
print("*args")

def func(*args):
    print(type(args).__name__)
    print(args)

# *args is not named arguments unlike **kwargs
# func(t = ('a', 'b', 'g'))

# *args is tuple elements
func('alpha', 'beta', 'gamma')
func(1)
func('A')
func(True)
func()
func(None) # Works unlike ruby array(Nil)
print("\n")

# *args is tuple of tuples
ta = ('a', 'b', 'g')
func(ta)
tn = (1, 2, 3)
func(ta, tn)      
print("\n")


# *args, **kwargs
print("*args, **kwargs")
def example(*args, **kwargs):    
    print(type(args).__name__)
    print(args)
    print(type(kwargs).__name__)
    print(kwargs)    
example("Hello", " ", w = "World", ex = "!")
print()

def arg(*args):    
    for count, item in enumerate(args):
        print("%d - %s" % (count, item))        
arg('alpha', 'beta', 'gamma')
print()

def kwarg(**kwargs):    
    for key, value in kwargs.items():
        print("%s = %s" % (key, value))
kwarg(a = 'alpha', g = 'gamma', b = 'beta')
print()

kwarg(d = {'a': 'alpha', 'g': 'gamma', 'b': 'beta',})

def function(*args, **kwargs):
    print(type(args).__name__)
    print(args)
    print(type(kwargs).__name__)
    print(kwargs)

print("\n")


# **kwargs
print("**kwargs")
def func(**kwargs):
    print(type(kwargs).__name__)
    print(kwargs)

# **kwargs is always named arguments (unlike *args) and dictionary
d = {'alpha': 1, 'beta': 2, 'gamma': 3}
# func(d)

# **kwargs is always named arguments (unlike *args) and dictionary elements
func(d=1)
print()
func(d1=1, d2=2)
print()

# **kwargs is always named arguments (unlike *args) and dictionary of dictionaries 
func(a={'alpha': 1, 'beta': 2, 'gamma': 3})
print()
func(n = {1: 'alpha', 2: 'beta', 3: 'gamma'})
print()
func(a={'alpha': 1, 'beta': 2, 'gamma': 3}, n = {1: 'alpha', 2: 'beta', 3: 'gamma'})
print("\n")


# builtin functions
print("builtin functions")
import sys

print(globals())

print(locals())

help("pydoc") #
import pydoc #
help(pydoc) #

print(eval("2 if not True else 1"))

print(eval("sys.version_info.micro"))

exec("print('Executing Python print command')")

exec("print('Executing Python print command with globals(), locals()')", globals(), locals())

help("exec")

import types
import collections
import builtins

ODict = collections.OrderedDict

def show_builtins():

    keys = ("Warnings", "Exceptions", "Types", "Functions", "Others")
    objs = dict(zip(keys, (ODict() for i in keys)))

    for name in dir(builtins):
        if name in ("__doc__", "__name__", "__package__"):
            continue

        obj = getattr(builtins, name)
        _repr = "<{} object>".format(type(obj).__name__)
        if isinstance(obj, type):
            if issubclass(obj, Warning):
                objs["Warnings"][name] = obj
            elif issubclass(obj, Exception):
                objs["Exceptions"][name] = obj
            else:
                objs["Types"][name] = obj
        elif callable(obj):
            if isinstance(obj, types.FunctionType):
                objs["Functions"][name] = obj
            else:
                objs["Functions"][name] = _repr
        else:
            objs["Others"][name] = _repr

    for key in keys:
        section_name = " Builtin {}:".format(key)
        print()
        print(section_name)
        print("-"*(len(section_name)+1))
        for name, obj in objs[key].items():
            print("{:<21} {}".format(name, obj))

show_builtins()

print("\n")


# *args class callable
print("*args class callable")
def func(*args):
   print(type(args).__name__)
   class Bindargs(object):
       foo = args[0]
       print("foo is", foo)
       def __init__(self, args):
          print("init Bindargs", args)
   return Bindargs # 'Bindargs' object is callable

f = func(3,)
f(args="bar") #
f(None) #
f("") #
f(1) #
f(True) #
print()

# **kwargs class callable
print("**kwargs class callable")
def function(**kwargs):
   print(type(kwargs).__name__)
   class Bindkwargs(object):
       foo = kwargs["foo"]
       print("foo is", foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)
   return Bindkwargs # 'Bindkwargs' object is callable

f = function(foo=3)
f(kwargs="bar") #
f(None) #
f("") #
f(1) #
f(True) #
print()

# Note
print("Note")
def method(*args, **kwargs):
   print("*args is ", type(args).__name__)
   print("**kwargs is ", type(kwargs).__name__)
method()

print("\n")


# *args class instance
print("*args class instance")
def func(*args):
   print(type(args).__name__)
   class Bindargs(object):
       foo = args[0]
       print("foo is", foo)
       def __init__(self, args):
          print("init Bindargs", args)
   return Bindargs(args) # return an instance of the class # 'Bindargs' object is not callable

func(3,)
print()

# **kwargs class instance
print("**kwargs class instance")
def function(**kwargs):
   print(type(kwargs).__name__)
   class Bindkwargs(object):
       foo = kwargs["foo"]
       print("foo is", foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)
   return Bindkwargs(kwargs) # return an instance of the class # 'Bindkwargs' object is not callable

function(foo=3)
print()

# Note
print("Note")
def method(*args, **kwargs):
   print("*args is ", type(args).__name__)
   print("**kwargs is ", type(kwargs).__name__)
method()

print("\n")


# class inside method
print("class inside method")
def func():
    x = 3
    class FuncClass(object):
        y = x
    return FuncClass

f = func()
print(callable(f))
print(f.y)
print(f().y)
print()

def function():
    x = 3
    class FunctionClass(object):
        y = x
    return FunctionClass()

f = function()
print(callable(f))
print(f.y)

print("\n")


# callable class inside method
print("callable class inside method")

def func(**kwargs):
   class Bindkwargs(object):
       foo = kwargs['foo']
       print('foo is', foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)          
   return Bindkwargs # 'Bindkwargs' object is callable

f = func(foo=3)
f(kwargs="bar") #
f(None) #
f("") #
f(1) #
f(True) #

print("\n")


# return instance of class from method
print("return instance of class from method")

def func(**kwargs):
   class Bindkwargs(object):
       foo = kwargs['foo']
       print('foo is ', foo)
       def __init__(self, kwargs):
          print("init Bindkwargs", kwargs)
   return Bindkwargs(kwargs) # return an instance of the class # 'Bindkwargs' object is not callable

func(foo=3)