print(9/2) # floating point division # 4 in Python 2.7 and 4.5 in Python 3.5
print(9//2) # floor division # 4 in Python 2.7 and Python 3.5
print("")


# Complex numbers are written in the form, x + yj, where x is the real part and y is the imaginary part.
print("complex")
c = 5 + 3j
print(c)
print(type(c))   
print(isinstance(c, complex))
print("c + 10")
print(c + 10)
print("")

print("Binary Prefix '0b' or '0B'")
print("b = 0b11111111")
b = 0b11111111
print(b)

print("type(b)")
print(type(b))

print("int(b)")
print(int(b))

print("b + 10")
print(b + 10)
print("")

print("Octal Prefix '0o' or '0O'")
print("o = 0o11111111")
o = 0o11111111
print(o)

print("type(o)")
print(type(o))

print("int(o)")
print(int(o))

print("o + 10")
print(o + 10)
print("")

print("Hexadecimal Prefix '0x' or '0X'")
print("h = 0x11111111")
h = 0x11111111
print(h)

print("type(h)")
print(type(h))

print("int(h)")
print(int(h))

print("h + 10")
print(h + 10)
print("")


import random
print("random.randrange(10, 20)")
print(random.randrange(10, 20))

x = ['a', 'b', 'c', 'd', 'e']
print("x")
print(x)
print("random.choice(x)")
print(random.choice(x))
print("random.shuffle(x)")
random.shuffle(x)
print(x)
print("random.random()")
print(random.random())
