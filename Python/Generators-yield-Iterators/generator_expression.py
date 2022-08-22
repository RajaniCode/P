from __future__ import print_function

x = "Hello World!"
# x = [1, 2, 3]

generator = (x[i] for i in range(len(x) -1, -1, -1))

for i in generator:
    print(i,  end="")
