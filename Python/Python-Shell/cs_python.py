def getenumerator():
    for i in range(100):
        if i < 20 and i % 2 == 0:
            yield i

ienumerable = getenumerator()

for i in ienumerable:
    print i

            
