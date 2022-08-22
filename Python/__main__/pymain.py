if __name__ == "__main__":
    print('This program is being run by itself')
else:
    print('I am being imported from another module')

print(__name__)

'''
This program is being run by itself
__main__
>>> import pymain
I am being imported from another module
pymain
>>> 
'''
