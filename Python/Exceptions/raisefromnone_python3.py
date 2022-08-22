class Example(object):
    def __getattribute__(self, item):
        self.dict  = { "A": "Alpha", "B": "Beta", "G": "Gamma"}
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            pass  # fallback to dict
        try:
            return self.dict[item]
        except KeyError:
            raise AttributeError("The object doesn't have such attribute") #
            # Only in Python 3.5
            # raise AttributeError("The object doesn't have such attribute") from None

eg = Example()
print(eg.__getattribute__('A'))
print(eg.__getattribute__('B'))
print(eg.__getattribute__('C'))


