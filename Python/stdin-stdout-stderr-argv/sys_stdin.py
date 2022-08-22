import sys

# Python 2.7 only numeric values and boolean
x = input("read via input(): ")
print("your input via input(): %s" % x)

# Python 3 'raw_input' is not defined
y = raw_input("read via raw_input(): ")
print("your input via raw_input(): %s" % y)

print("read via sys.stdin.readline()[:-1]")
print("your input via stdin.readline()[:-1]: %s" % sys.stdin.readline()[:-1])


'''
Python 2.7

read via input(): 2/2
your input via input(): 1
read via raw_input(): 2/2
your input via raw_input(): 2/2
read via sys.stdin.readline()[:-1]
2/2
your input via stdin.readline()[:-1]: 2/2

Python 3

read via input():  2/2
your input via input(): 2/2
read via sys.stdin.readline()[:-1]
 2/2
your input via stdin.readline()[:-1]: 2/2

'''
