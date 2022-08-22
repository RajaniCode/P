'''from __future__ import print_function

for item in [1,2,3,4]:
    print(item, " ", end="")'''


print '123',
print '\b456'

print "123",
print "456"

print("")

for i in range(65, 91, 1):
    print("Ascii value of %s = %d" % (chr(i), ord(chr(i))))

print("")

for i in range(97, 123, 1):
    print("Ascii value of %s = %d" % (chr(i), ord(chr(i))))

print("")

x = "\\"
y = "b"
z = x + y
print z

print("")

h = "Hello"
w = "World!"

print("%s %s" % (h, w))
print("{} {}".format(h, w))
print(' '.join([h, w]))
print(h + " " + w)
    
# Only in Python 2.7
'''
for i in range(65, 91, 1):
    print(unichr(i))

print("")

# Only in Python 2.7
for i in range(97, 123, 1):
    print(unichr(i))
'''

