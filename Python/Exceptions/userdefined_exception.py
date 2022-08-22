class ValueBigError(Exception):
    pass

class ValueSmallError(Exception):
    pass

class Example(object):
    def func(cls):
        while True:
            try:
                f = float(input("Enter number: "))
                if f >= 100:
                    raise ValueBigError
                elif f <= -10:
                    raise ValueSmallError
                break
            except ValueBigError as vbe:
                print("Number is too big, please enter again")
                print("")
            except ValueSmallError as vse:
                print("Number is too small, please enter again")
                print("")
        x = str(f).split('.')        
        # print len(x[1])
        # print x[1]
        y = abs(int(x[0])) if (int(x[0]) == 0) else int(x[0])
        z = y if (len(x[1]) == 1 and int(x[1]) == 0) else f        
        print("Thank you for entering correct number: " + str(z))

eg = Example()
eg.func()
