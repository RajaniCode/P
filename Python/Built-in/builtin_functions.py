import sys

print(globals())

print(locals())

help("pydoc") #
import pydoc #
help(pydoc) #

print(eval("2 if not True else 1"))

print(eval("sys.version_info.micro"))

exec("print('Executing Python print command')")

exec("print('Executing Python print command with globals(), locals()')", globals(), locals())

help("exec")
