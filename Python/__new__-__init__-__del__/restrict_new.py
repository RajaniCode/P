class Restricted(object):
    MAX_Instance = 4
    CLS_Instance = 0
    def __new__(cls):
        if(cls.CLS_Instance >= cls.MAX_Instance):
            raise ValueError("Cannot create more objects")
        cls.CLS_Instance += 1
        return object.__new__(cls)

a = Restricted()
b = Restricted()
c = Restricted()
d = Restricted()
#
e = Restricted()

