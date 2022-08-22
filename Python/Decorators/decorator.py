def prettify(func):
    def inner():
        print "I got pretty"
        func() # Note function call
    return inner

@prettify
def normal():
    print "I am normal"
normal()

# is equivalent to
'''def normal():
    print "I am normal"
pret = prettify(normal)
pret()'''
