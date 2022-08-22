# abstractplugin_register.py
from __future__ import print_function
from abstract_plugin import Plugin

class RegisteredImplementation(object):
    def load(self, obj):
        return obj.read()
    def save(self, output, data):
        return output.write(data)

Plugin.register(RegisteredImplementation)

if __name__ == '__main__':
    print('Subclass:', issubclass(RegisteredImplementation, Plugin))
    print('Instance:', isinstance(RegisteredImplementation(), Plugin))


        
