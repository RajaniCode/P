def countdown(n):
    print("counting down")
    while n >= 9:
        yield n
        n -= 1
    return

for x in countdown(10):
    print(x) # 10, 9

print("Post Iteration")

c = countdown(10)
next(c) # 10
next(c) # 9
next(c) 

