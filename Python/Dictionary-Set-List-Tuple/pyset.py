A = { 1, 2, 3, 4, 5 }
B = { 4, 5, 6, 7, 8 }
S = set([1, 2, 3, 4, 5])

print("A")
print(A)
print("")

print("B")
print(B)
print("")

print("S")
print(S)
print("")

print("type(A).__name__")
print(type(A).__name__)
print("")

print("type(B).__name__")
print(type(B).__name__)
print("")

print("type(S).__name__")
print(type(S).__name__)
print("")

print("A | B or A.union(B)")
print(A | B)
print("")

print("A | B or A.union(B)")
print(A.union(B))
print("")

print("A & B or A.intersection(B)")
print(A & B)
print("")

print("A & B or A.intersection(B)")
print(A.intersection(B))
print("")

print("A - B or A.difference(B)")
print(A - B)
print("")

print("A - B or A.difference(B)")
print(A.difference(B))
print("")

print("A ^ B or A.symmetric_difference(B) or A.union(B).difference(A.intersection(B)) or (A | B) - (A & B)")
print(A ^ B)
print("")

print("A ^ B or A.symmetric_difference(B) or A.union(B).difference(A.intersection(B)) or (A | B) - (A & B)")
print(A.symmetric_difference(B))
print("")

print("A ^ B or A.symmetric_difference(B) or A.union(B).difference(A.intersection(B)) or (A | B) - (A & B)")
print(A.union(B).difference(A.intersection(B)))
print("")

print("A ^ B or A.symmetric_difference(B) or A.union(B).difference(A.intersection(B)) or (A | B) - (A & B)")
print((A | B) - (A & B))
print("")

print("A.add(9)")
A.add(9)
print(A)
print("")

print("A.update([8])")
A.update([8])
print(A)
print("")

print("A.update([9, 10])")
A.update([9, 10])
print(A)
print("")

print("A.discard(9)")
A.discard(9)
print(A)
print("")

print("A.discard(9)")
A.discard(9)
print(A)
print("")

print("A.remove(10)")
A.remove(10)
print(A)
print("")

# Error if not exists
'''
print("A.remove(10)")
A.remove(10)
print(A)
print("")
'''

print("A.pop()")
A.pop()
print(A)
print("")

print("A.clear()")
A.clear()
print(A)
print("")

print("C = B.copy()")
C = B.copy()
print("B")
print(B)
print("C")
print(C)
print("")

print("B == C")
print(B == C)
print("")

print("C == B")
print(C == B)
print("")

print("B is C")
print(B is C)
print("")

print("C is B")
print(C is B)
print("")

print("D = B")
D = B
print(D)
print("")

print("B == D")
print(B == D)
print("")

print("D == B")
print(D == B)
print("")

print("B is D")
print(B is D)
print("")

print("D is B")
print(D is B)
print("")

F = frozenset([1, 2, 3, 4])
print("F")
print(F)
print("")

G = frozenset([3, 4, 5, 6])
print("G")
print(G)
print("")

print("F | G or F.union(G)")
print(F | G)
print("")

print("F | G or F.union(G)")
print(F.union(G))
print("")

print("F & G or F.intersection(G)")
print(F & G)
print("")

print("F & G or F.intersection(G)")
print(F.intersection(G))
print("")

print("F - G or F.difference(G)")
print(F - G)
print("")

print("F - G or F.difference(G)")
print(F.difference(G))
print("")

print("# Note: 'frozenset' object has no attribute 'add', 'remove', 'update' etc")

print("F")
print(F)
print("")

print("type(F)")
print(type(F))
print("")

H = ([1, 2, 3, 4])
print("H")
print(H)
print("")

print("type(H)")
print(type(H))
print("")
