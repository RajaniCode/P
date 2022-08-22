import sys
import random

try:
    # Only in Python 2.7
    x = int(raw_input("Enter Number: "))
    # For ValueError in Python 3.5
    # x = int(input("Enter Number: "))
    r = random.randint(1, 10)  / x
    y = r / float(x) 
except(ValueError, ZeroDivisionError) as e:
    print("Error: %s" % repr(e))
# except:
    # print("Unexpected error:", sys.exc_info()[0])
    # raise'''
else:
    print("Random integer %d divided by input %d = %f" % (r, x, y))
finally:
    print("Executing finally clause")
