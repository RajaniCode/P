def exceptional_divide(func):
    def inner(x, y):
        print("Gonna divide {} by {}".format(x, y))
        if y == 0:
            print("Whoops! Cannot divide {} by {}".format(x, y))
            return # Note return
        return func(x, y) # Note return function call with parameter
    return inner

@exceptional_divide
def divide(x, y):
    return x / y

divide(5, 2)

divide(5, 0)
