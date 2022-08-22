def func():
    try:
        raise RuntimeError("To Force Issue")
    except:
        return 1
    else:
        return 2
    finally:
        return 3

def function():
    try:
        try:
            raise RuntimeError("To Force Issue")
        except:
            return 10
        else:
            return 20
        finally:
            return 30
    except:
        print(40)
    else:
        print(50)
    finally:
        print(60)
        
print(func())

print(function())
