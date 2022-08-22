class Foo:
  def __call__(self):
    print('called')

foo_instance = Foo()
foo_instance() #this is calling the __call__ method


class Add:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        print "Sum of", self.num1,"and",self.num2, "is:"
     
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

