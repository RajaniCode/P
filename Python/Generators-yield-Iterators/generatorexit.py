def countdown(n):
    print("Counting down from %d" % n)
    try:
        while n > 0:
            yield n
            n = n - 1
    except GeneratorExit:
        print("Only made it to %d" % n)

c = countdown(10)
next(c) # Only made it to 10
next(c) # Only made it to 9
next(c) # Only made it to 8
next(c) # Only made it to 7
next(c) # Only made it to 6
next(c) # Only made it to 5
next(c) # Only made it to 4
next(c) # Only made it to 3
next(c) # Only made it to 2
next(c) # Only made it to 1 with close()
c.close() # Only made it with close() and while n > 0
