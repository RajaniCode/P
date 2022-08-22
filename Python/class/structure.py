import struct

a = 1
b = b"alpha"
c = 2.3

packed = struct.pack('i 5s d', a, b, c)

a = 4
b = b"gamma"
c = 5.6

print(struct.unpack('i 5s d', packed))
