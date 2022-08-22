# Filename: pymodule.py

class Alpha(object):
    @staticmethod
    def static_method():
        if __name__ == '__main__':
            print('This static method is being run by itself')
        else:
            print('This static method is being imported from another module')
    @classmethod
    def class_method(cls):
        if __name__ == '__main__':
            print('This class method is being run by itself')
        else:
            print('This class method is being imported from another module')
    def instance_method(self):
        if __name__ == '__main__':
            print('This instance method is being run by itself')
        else:
            print('This instance method is being imported from another module')
            
