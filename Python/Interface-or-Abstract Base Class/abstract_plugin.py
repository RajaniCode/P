# abstract_plugin.py
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


        
