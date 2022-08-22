# https://leemendelowitz.github.io/blog/any-all-in-python.html

x = [-5, -4, -3, -2, -1, 0]
x = [-5, -4, -3, -2, -1]
print("print(all(i < 0 for i in [-5, -4, -3, -2, -1]))")
print(all(i < 0 for i in x))
print("")

x = [0, 1, 2, 3, 4, 5]
x = [-1, 0, 1, 2, 3, 4, 5]
print("print(all(i < 0 for i in [-1, 0, 1, 2, 3, 4, 5]))")
print(any(i < 0 for i in x))
print("")

print("all(l == 't' for l in 'python')")
print(all(l == 't' for l in 'python'))
print("")

print("any(l == 't' for l in 'python')")
print(any(l == 't' for l in 'python'))
print("")

g = (l == 't' for l in 'python')
any(g)
any( (l == 't' for l in 'python') ) # same as any(g)

print("generator = (l == 't' for l in 'python') next()")
generator = (l == 't' for l in 'python')
# .next() Only in Python 2.7
print(next(generator)) # False. 'p' is not equal to 't'
print(next(generator)) # False. 'y' is not equal to 't'
print(next(generator)) # True. 't' is equal to 't'
print("")

print("generator = (l == 't' for l in 'python')")
generator = (l == 't' for l in 'python')
for value in generator:
    print(value)
print("")

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
test_all() # Calls t(), then f(), then stops

def test_any():
    # Pass a generator expression with function calls to any
    print(any(func() for func in funcs))
test_any() # Calls t() once and stops.


