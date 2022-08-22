import sys

def func1():
    func2()

def func2():
    raise Exception('Test Error')

def func():
    err = None
    print("Begin try-except")
    try:
        func1()
    except:
        err = sys.exc_info()[1]
        pass
    print("End try-except")
    # some extra processing, involving checking err details (if err is not None)
    
    # need to re-raise err so caller can do its own handling
    if err:
        # Python has no way of knowing if err was an exception just caught before, or a new exception with a new stack trace
        # raise err # Wrong
        # A blank raise raises the last exception
        raise # Right
func()
