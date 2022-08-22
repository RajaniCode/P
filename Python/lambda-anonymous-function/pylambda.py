from functools import reduce
square = lambda x: x * x
print(square(4))
print("")

lst = [1, 5, 4, 6, 8, 11, 3, 12]

#Only in Python 2.7
# filter_lambda = filter(lambda x: x % 2 == 0, lst)
filter_lambda = list(filter(lambda x: x % 2 == 0, lst))
print(filter_lambda )
print(type(filter_lambda).__name__)
print("")

#Only in Python 2.7
#map_lambda = map(lambda x: x * 2, lst)
map_lambda = list(map(lambda x: x * 2, lst))
print(map_lambda )
print(type(filter_lambda).__name__)
print("")

print("fibonacci")
fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
print(fibonacci)
odd_fibonacci = list(filter(lambda x: x % 2, fibonacci))
print(odd_fibonacci) # [1, 1, 3, 5, 13, 21, 55]
even_fibonacci = list(filter(lambda x: x % 2 == 0, fibonacci))
print(even_fibonacci) # [0, 2, 8, 34]
# or alternatively:
even_fibonacci = list(filter(lambda x: x % 2 -1, fibonacci))
print(even_fibonacci) # [0, 2, 8, 34]
print("")

print("maximum of a list of numerical values [47, 11, 42, 102, 13] by using reduce")
lst = [47, 11, 42, 102, 13]
# from functools import reduce
reduce_lambda = reduce(lambda x, y: x if (x > y) else y, lst)
print(reduce_lambda)
print(type(reduce_lambda).__name__)
print("")

print("sum of the numbers from 1 to 100")
# from functools import reduce
reduce_lambda = reduce(lambda x, y: x + y, range(1, 101))
print(reduce_lambda)
print(type(reduce_lambda).__name__)
