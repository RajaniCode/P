class C(object):
    x = 1

class D(object):
    x = 2

class DerivedMultiple(C, D, object):
    def print_c(self):
        c = C()
        d = D()
        c.x = 1
        d.x = 2
        derived_multiple = DerivedMultiple();
        print("c.x = %d\n" % (c.x))
        print("d.x = %d\n" % (d.x))
        print("multiple_derived.x = %d\n" % (derived_multiple.x))

DerivedMultiple().print_c()

