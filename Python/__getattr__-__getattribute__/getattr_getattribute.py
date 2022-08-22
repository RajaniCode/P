class Dictionary(object):
    def __init__(self):
        self.x = 1
        self.y = 2
    # def __getattr__(self, name):
    def __getattribute__(self, name): #
        if name == 'x':
            return 0
        else:
            return object.__getattribute__(self, name)

d = Dictionary()

print(d.x)
print(d.y)
