lst = ["Hello", "World!"]

# Generators are an incredible powerful programming construct. They allow you to write streaming code with fewer intermediate variables and data structures. Besides that, they are more memory and CPU efficient. Finally, they tend to require fewer lines of code, too.
# Tip to get started with generators: find places in your code where you do the following:

'''
def something():
    result = []
    for item in lst:
        result.append(item)
    return result
'''

# And replace it by:
 
def iter_something():
    for item in lst:
        yield item

def something():  # Only if you really need a list structure
    return list(iter_something())

print(something())
