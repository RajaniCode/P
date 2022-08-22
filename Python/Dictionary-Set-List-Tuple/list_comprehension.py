class Obj(object):
    id = 0

obj0 = Obj()
obj0.id = 100

obj1 = Obj()
obj1.id = 101

obj2 = Obj()
obj2.id = 102

objs = [obj0, obj1, obj2]

ids = [obj.id for obj in objs if obj.id > 100]
print ids

dictids = {obj.id for obj in objs if obj.id > 100}
print dictids


dictlc = {x: x*x for x in range(6)}
print dictlc


