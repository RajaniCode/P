def multiplier(n):
    def times(x):
        return n * x
    return times

times3 = multiplier(3)
print(times3(6))

times5 = multiplier(5)
print(times5(10))

del multiplier

print(times5(20))


