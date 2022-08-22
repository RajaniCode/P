import sys, traceback

def excepthook(type, value, tb):
    traceback.print_exception(type, value, tb)

    while tb.tb_next:
        tb = tb.tb_next

    # Only in Python 2.7
    # print >>sys.stderr, 'Locals:',  tb.tb_frame.f_locals
    # print >>sys.stderr, 'Globals:', tb.tb_frame.f_globals
    sys.stderr.write('Locals:',  tb.tb_frame.f_locals)
    sys.stderr.write('Globals:', tb.tb_frame.f_globals)

sys.excepthook = excepthook

def x():
    y()

def y():
    foo = 1
    bar = 0
    foo/bar

x()

# Note
'''
To print vars from each frame in a traceback, change the above loop to

    while tb:
        print >>sys.stderr, 'Locals:',  tb.tb_frame.f_locals
        print >>sys.stderr, 'Globals:', tb.tb_frame.f_globals
        tb = tb.tb_next
'''
