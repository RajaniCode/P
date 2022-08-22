class Example:
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

eg = Example()
eg.x = 1
print(eg.x)
eg.x = "This is property in Python"
print(eg.x)


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


    
