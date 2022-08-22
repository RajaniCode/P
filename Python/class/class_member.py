class C(object):
    x = 0

class Program(object):
    def print_c(self):
        a = C()
        b = C()
        a.x = 1
        b.x = 2
        print("Class Before a = b: a.x = %d, b.x = %d\n" % (a.x, b.x))
        a = b
        a.x = 3
        print("Class After a = b and a.x = 3: a.x = %d, b.x = %d\n" % (a.x, b.x)) # 3, 3

Program().print_c()

