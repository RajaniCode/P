from itertools import count, cycle, islice

# help("itertools")

print("count:")
counter = count(start=13)
print(next(counter))
print(next(counter))
print("")

print("cycle:")
colors = cycle(['red', 'white', 'blue'])
print(next(colors))
print(next(colors))
print(next(colors))
print(next(colors))
print("")

print("islice:")
colors = cycle(['red', 'white', 'blue'])  # infinite
limited = islice(colors, 0, 4)            # finite

for x in limited: # so safe to use for-loop on
    print(x)
print("")

print("Fibonacci numbers islice:")
class fib:
    def __init__(self):
        self.prev = 0
        self.curr = 1
    def __iter__(self):
        return self    
    def next(self): # Python 3.5 def __next__(self):
        value = self.curr
        self.curr += self.prev
        self.prev = value
        return value
    
f = fib()
print(list(islice(f, 0, 20)))
print(list(islice(f, 0, 10)))
print("")
