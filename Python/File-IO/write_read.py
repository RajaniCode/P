# https://docs.python.org/2/tutorial/inputoutput.html

f = open('file.txt', 'w') #
f = open('file.txt', 'r+') # existing file
f.write('0123456789abcdef')

f.seek(5)     # Go to the 6th byte in the file
print(f.read(1)) # 5

f.seek(-4, 2)  # Go to the 4th byte before the end
print(f.read(1)) # c
print(f.read(1)) # d
print(f.read(2)) # ef
f.close()


