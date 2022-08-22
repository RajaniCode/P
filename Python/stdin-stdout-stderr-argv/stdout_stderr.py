import sys

for i in range(3):
    print("Hello World!")

for i in range(3):
    sys.stdout.write("Hello World!\n") #Note: \n

# sys.stdout.flush()

for i in range(3):
    sys.stderr.write("Hello World!\n") #Note: \n

# sys.stderr.flush()
