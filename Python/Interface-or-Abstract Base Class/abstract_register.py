from __future__ import print_function
import abc

# Python 3.5
# class Plugin(metaclass=abc.ABCMeta):    
class Plugin(object):
    __metaclass__ = abc.ABCMeta #
    @abc.abstractmethod
    def load(self, obj):
        """Retrieve data from the source and return an object"""
        return
    @abc.abstractmethod
    def save(self, output, data):
        """Save the data object to the output"""

class RegisteredImplementation(object):
    def load(self, obj):
        return obj.read()
    def save(self, output, data):
        return output.write(data)

Plugin.register(RegisteredImplementation)

if __name__ == '__main__':
    print('Subclass:', issubclass(RegisteredImplementation, Plugin))
    print('Instance:', isinstance(RegisteredImplementation(), Plugin))


        
