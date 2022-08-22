class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return "(%d,%d)" % (self.x, self.y)
    def __add__(self, obj):
        x = self.x  + obj.x
        y = self.y  + obj.y
        return Point(x, y)
        
p1 = Point(2, 3)
p2 = Point(4, 6)
print(p1)
print(p2)
print(p1 + p2)
