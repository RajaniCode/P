import sys

def divide(x, y):
    try:
       return x / float(y)
    except:
        print("Error: %s" % sys.exc_info()[0])
    else:
        print("No Error")
    finally:
        print("Exiting finally")

print(divide(1, 2))
print("")
print(divide(1, 0))
