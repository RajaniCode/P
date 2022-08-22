from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs)

print("Test")

# The function eprint can be used in the same was as the standard print function:
# stdout
eprint("Test")
eprint("foo", "bar", "baz", sep="---")
    
