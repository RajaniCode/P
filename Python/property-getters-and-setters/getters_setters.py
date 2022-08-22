class GettersSetters(object):
    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

gs = GettersSetters()
gs.set_x(2)
print(gs.get_x())
gs.set_x("This is getters and setters in Python")
print(gs.get_x())


    
