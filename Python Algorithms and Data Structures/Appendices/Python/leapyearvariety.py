#-----------------------------------------------------------------------
# leapyearvariety.py
#-----------------------------------------------------------------------

import stdio
import sys

# Accept a year as a command-line argument. Write True to standard
# output if the year is a leap year in the Gregorian calendar, and
# False otherwise.

year = int(sys.argv[1])

a = (((year % 4) == 0) and ((year % 100) != 0)) or ((year % 400) == 0)
b = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
c = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
d = year % 4 == 0 and year % 100 != 0 or year % 400 == 0
e = ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0)

stdio.writeln(a)
stdio.writeln(b)
stdio.writeln(c)
stdio.writeln(d)
stdio.writeln(e)

#-----------------------------------------------------------------------

# python leapyearvariety.py 2016
# True
# True
# True
# True
# True

# python leapyearvariety.py 1900
# False
# False
# False
# False
# False

# python leapyearvariety.py 2000    
# True
# True
# True
# True
# True