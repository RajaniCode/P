def asterisk(func):
    def inner(*args, **kwargs):
        print("*" * 12)
        func(*args, **kwargs) # Note function call with parameters
        print("*" * 12)
    return inner

def percent(func):
    def inner(*args, **kwargs):
        print("%" * 12)
        func(*args, **kwargs) # Note function call with parameters
        print("%" * 12)
    return inner

@asterisk
@percent
def printer(msg):
    print(msg)
printer("Hello World!")

# is equivalent to 
'''
def printer(msg):
    print(msg)
printer = asterisk(percent(printer))
printer("Hello World!")
'''
