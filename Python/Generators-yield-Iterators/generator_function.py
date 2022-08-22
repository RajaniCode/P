from __future__ import print_function # print(c, end="")
# import sys

def generator(x):
    for i in range(len(x) -1, -1, -1):
        yield x[i]

x = "Hello World!"
# x = [1, 2, 3]

g = generator(x)

for c in g:
    print(c, end="")
    # sys.stdout.write(c)

# sys.stdout.flush()
    

