class C(object):
    def __init__(self):
        self.x = 0
        self._x = 1
        self.__x = 2

class Derived(C):
    def _print_c(self):        
        base_instance = C()
        derived_instance = Derived()
        print("Access protected member in derived class with base class instance: %d\n" % (base_instance._x))
        print("Access protected member in derived class with derived class instance: %d\n" % (derived_instance._x)) 

class FurtherDerived(Derived):
  def print_c(self):
    super()._print_c()
    
FurtherDerived().print_c()

base_instance = C()

print("Access (but not advised) protected member outside its scope with base class instance: %d\n" % (base_instance._x))
derived_instance = Derived()
print("Access (but not advised) protected member outside its scope with derived class instance: %d\n" % (derived_instance._x))
further_derived_instance = FurtherDerived()
print("Access (but not advised) protected member outside its scope with further derived class instance: %d\n" % (further_derived_instance._x))

class AccessProtected:
  def print_c(self):
    print("Access (but not advised) protected method outside its scope")
    Derived()._print_c()
    
AccessProtected().print_c()



