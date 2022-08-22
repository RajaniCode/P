# Non Unique
lst = ['alpha', 'beta', 'gamma' , 'delta', 'epsilon', 'beta', 'zeta', 'greek', 'gamma', 'eta', None, 1, 'theta', 'latin']

print("type(lst).__name__")
print(type(lst).__name__)
print(lst)
print(len(lst))
print("")

print("lst.append('iota')")
lst.append('iota')
print(lst)
print(len(lst))
print("")

print("lst.remove('greek')")
lst.remove('greek')
print(lst)
print(len(lst))
print("")

print("lst.remove(1)")
lst.remove(1)
print(lst)
print(len(lst))
print("")

print("lst.pop()")
lst.pop()
print(lst)
print(len(lst))
print("")

print("lst.pop(5)")
lst.pop(5)
print(lst)
print(len(lst))
print("")

print("del lst[6]")
del lst[6]
print(lst)
print(len(lst))
print("")

print("lst.insert(9, 'kappa')")
lst.insert(9, 'kappa')
print(lst)
print(len(lst))
print("")

print("lst[10] = 'lambda'")
lst[10] = 'lambda'
print(lst)
print(len(lst))
print("")

print("lst.insert(len(lst), 'mu')")
lst.insert(len(lst), 'mu')
print(lst)
print(len(lst))
print("")

print("lst.remove(None)")
lst.remove(None)
print(lst)
print(len(lst))
print("")

print("lst.insert(8, 'iota')")
lst.insert(8, 'iota')
print(lst)
print(len(lst))
print("")

l = ['nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']

print("lst.extend(l)")
lst.extend(l)
print(lst)
print(len(lst))
print("")

print("le = lst")
le = lst
print("")

print("le == lst")
print(le == lst)
print("")

print("lst == le")
print(lst == le)
print("")

print("le is lst")
print(le is lst)
print("")

print("lst is le")
print(lst is le)
print("")

#Python 3.5
'''

print("lc = lst.copy()")
lc = lst.copy()
print("")

print("lc == lst")
print(lc == lst)
print("")

print("lst == lc")
print(lst == lc)
print("")

print("lc is lst")
print(lc is lst) # False
print("")

print("lst is lc")
print(lst is lc) # False
print("")

'''
