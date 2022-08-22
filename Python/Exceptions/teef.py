def func():
    try:        
        # raise RuntimeError, "To Force Issue" # Only in Python 2.7
        raise RuntimeError("To Force Issue")
    except:
        return 1
    else:
        return 2
    finally:
        return 3

def nested():
    try:
        try:            
            # raise RuntimeError, "To Force Issue" # Only in Python 2.7
            raise RuntimeError("To Force Issue")
        except:
            return 4
        else:
            return 5
        finally:
            return 6
    except:
        print(7)
    else:
        print(8)
    finally:
        print(9)
        
print(func())

print(nested())
