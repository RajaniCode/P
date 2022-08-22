def increment(x):
    return x + 1

def decrement(x):
    return x - 1

# functions that take other functions as arguments are also called higher order functions
def operate(func, x):
    x = func(x)
    return x

print(operate(increment, 5))

print(operate(decrement, 5))

