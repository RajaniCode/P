import sys

while True:
    try:
        # Only in Python 2.7
        x = float(raw_input("Enter Number: "))
        # Python 3.5
        # x = float(input("Enter Number: "))
        break
    except:
        print("Error %s" % sys.exc_info()[0])
        print("")

print("The reciprocal of %d is %f" % (x, 1/x))

