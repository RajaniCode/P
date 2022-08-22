from __future__ import print_function # print(c, end="")
# import sys

def generator(x):
    for i in range(len(x) -1, -1, -1):
        yield x[i]

x = "Hello World!"
# x = [1, 2, 3]

iterable = generator(x)

'''for value in iterable:
    print(value, end="")'''

'''y = ""
for i in range(len(x)):
    y += next(iterable)
print(y)'''
 

done = object()


def createGenerator(aNext):
    while (aNext is done):
        yield aNext


g = createGenerator(iterable)

for i in g:
    print(i)
