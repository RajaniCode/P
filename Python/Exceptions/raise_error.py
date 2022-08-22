# Only in Python 2.7
'''try:
    n = int(raw_input("Enter positive integer: ")) 
    if n <= 0:
        raise ValueError, "This is not a positve integer"
except ValueError, ve:
    print "Error:", ve'''

try:
    n = int(input("Enter positive integer: ")) 
    if n <= 0:
        raise ValueError("This is not a positve integer")
except ValueError as ve:
    print("Error: %s" % ve)

