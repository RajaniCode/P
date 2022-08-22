# Non Unique
tpl = ('alpha', 'beta', 'gamma', 'beta')
print(type(tpl).__name__)
print(tpl)
print(len(tpl))
print("unpack")
print("(a, b, g, b) = tpl")
(a, b, g, b) = tpl
print("pack")
print("tpl = (a, b, g)")
tpl = (a, b, g)
print(type(tpl).__name__)
print(tpl)
print(len(tpl))
print("")

print("tuple from str split")
line = "alpha - beta - gamma - delta - epsilon - beta - zeta - greek - gamma - eta"
print(line)
print("unpack")
print("(a, b, g, d, e, b, z, g, g, e) =  line.split('-')")
(a, b, g, d, e, b, z, g, g, e) =  line.split('-')
print("x = (a, b, g, d, e, b, z, g, g, e)")
x = (a, b, g, d, e, b, z, g, g, e)
print(x)
print("")

print("empty tuple")
empty_tuple = ()
print(empty_tuple)
print("")

print("tuple having integers")
integer_tuple = (1, 2, 3)
print(integer_tuple)
print("")

print("tuple having integers # Non Unique")
integer_tuple = (1, 2, 3, 1)
print(integer_tuple)
print("")

print("tuple with mixed datatypes")
mixed_tuple = (1, "Hello", 3.4)
print(mixed_tuple)
print("")

print("nested tuple")
nested_tuple = ("mouse", [8, 4, 6], (1, 2, 3))
print(nested_tuple)
print("")

print("tuple can be created without parentheses, called tuple packing")
print("tuple_packing = 3, 4.6, 'dog'")
tuple_packing = 3, 4.6, 'dog'
print(tuple_packing)
print("")

print("tuple unpacking")
print("a, b, c = tuple_packing")
a, b, c = tuple_packing
print(a, b, c)
print("")

print("need a comma at the end otherwise it becomes str")
one_element = ("hello",)  
print(one_element)
print("")

print("parentheses is optional")
without_parentheses = "hello", 
print(without_parentheses)
print("")

# Tuples and list are similar except that tuple is immutable and list is mutable
list_tuple = ('p','y','t','h','o','n') # list_tuple = ['p','y','t','h','o','n'] 
print("type(list_tuple).__name__")
print(type(list_tuple).__name__)
print(list_tuple[0])
print("")
# IndexError: tuple index out of range
# print(list_tuple[6])

nested_tuple = ("python", [8, 4, 6], (1, 2, 3))
print("nested_tuple")
print(nested_tuple)
print("nested_tuple[0][3]")
print(nested_tuple[0][3])
print("nested_tuple[1][1]")
print(nested_tuple[1][1])
print("nested_tuple[2][0]")
print(nested_tuple[2][0])
print("")

print("negative indexing")
negative_tuple = ('p','y','t','h','o','n') # negative_tuple = ['p','y','t','h','o','n']
print("negative_tuple[-1]")
print(negative_tuple[-1])
print("negative_tuple[-6]")
print(negative_tuple[-6])
print("")

print("slicing")
list_tuple = ('p','y','t','h','o','n') # list_tuple = ['p','y','t','h','o','n']
print("elements 2nd to 4th")
print("list_tuple[1:4]")
print(list_tuple[1:4])
print("")

print("elements beginning to 2nd")
print("list_tuple[:-4]")
print(list_tuple[:-4])
print("")

print("elements 3rd to end")
print("list_tuple[2:]")
print(list_tuple[2:])
print("")

print("elements beginning to end")
print("list_tuple[:]")
print(list_tuple[:])
print("")

print("reverse")
print("list_tuple[::-1]")
print(list_tuple[::-1])
print("")


print("change_tuple")
change_tuple = (4, 2, 3, [6, 5]) # not list [4, 2, 3, [6, 5]]
print(change_tuple)
# TypeError: 'tuple' object does not support item assignment
# change_tuple[3] = 9
print("item of mutable element can be changed")
print("change_tuple[3][0] = 9")
change_tuple[3][0] = 9
print(change_tuple)
print("")

print("tuples can be reassigned")
print("change_tuple = ('p','y','t','h','o','n')")
change_tuple = ('p','y','t','h','o','n')
print(change_tuple)
print("")

print("tuples concatenation")
print("(1, 2, 3) + (4, 5, 6)")
print((1, 2, 3) + (4, 5, 6))
print("")

print("tuples times integer")
print("('python',) * 3")
print(('python',) * 3)
print("")

list_tuple = ('p','y','t','h','o','n') # list_tuple = ['p','y','t','h','o','n']
# TypeError: 'tuple' object doesn't support item deletion
# del list_tuple[3]
print("delete tuple")
print("del list_tuple")
del list_tuple
print("")

print("tuple methods")
tuple_method = ('a','p','p','l','e')
print("tuple_method.count('p')")
print(tuple_method.count('p'))
print("tuple_method.index('p')")
print(tuple_method.index('p'))
print("")

print("in or not in tuple")
print("'p' in tuple_method")
print('p' in tuple_method)
print("")

print("'p' not in tuple_method")
print('p' not in tuple_method)
print("")

print("'m' in tuple_method")
print('m' in tuple_method)
print("")

print("'m' not in tuple_method")
print('m' not in tuple_method)
print("")

print("for item in ('Foo','Bar'): print('Hello', item)")
for item in ('Foo','Bar'): print("Hello", item)
