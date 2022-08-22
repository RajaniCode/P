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

    
