import sys
import os

print(help(sys))
print("")

print(dir(sys))
print("")

for root, dirs, files in os.walk('.'):
    for name in files:
        print(name)
    for name in dirs:
        print(name)
