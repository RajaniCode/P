from __future__ import print_function

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
print("")

# *args is tuple of tuples
ta = ('a', 'b', 'g')
func(ta)
tn = (1, 2, 3)
func(ta, tn)


