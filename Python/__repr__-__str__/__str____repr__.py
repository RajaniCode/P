import gc

# class Node(object):
class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def addchild(self, node):
        self.parent = self
        self.children.append(node)

    def __repr__(self):
        return "<Node %s at %x>" % (repr(self.name), id(self))
    
    def __str__(self): # __str__ overrides __repr__
        return self.name

            
root = Node("Monty")

print(root)

root.addchild(Node("Eric"))
root.addchild(Node("John"))
root.addchild(Node("Michael"))

del root

print(gc.collect(), "unreachable objects")
print(gc.collect(), "unreachable objects")        
        
