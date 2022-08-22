from abc import ABCMeta, abstractmethod

# Python 3.5
# class Subs(metaclass=ABCMeta):
class Subs(object):
    __metaclass__ = ABCMeta

    default_ingredient = "Oats"

    @classmethod
    @abstractmethod
    def get_ingredient(cls):
        """Returns ingredient list"""
        return cls.default_ingredient

class HoneyOats(Subs):
    def get_ingredient(self):
        # return "Honey " + super().get_ingredient() # Only in Python 3.5 # Don't Repeat Yourself
        return "Honey " + super(HoneyOats, self).get_ingredient()

# Python 3.5 # Can't instantiate abstract class with abstract methods
# print(Subs().get_ingredient())
print(HoneyOats().get_ingredient())
