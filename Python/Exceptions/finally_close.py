'''
This way, we are guaranteed that the file is properly closed
even if an exception is raised, causing program flow to stop.
'''

try:
    fw = open("file.txt", "w")
    fw.write("Hello World!")
finally:
    fw.close()

try:
    fr = open("file.txt", "r")
    print(fr.read())
finally:
    fr.close()

'''
The best way to do this is using the with statement.
This ensures that the file is closed when the block inside with is exited.
We don't need to explicitly call the close() method. It is done internally.
'''

with open("file.txt", 'w') as f:
   f.write("Hello World!")

with open("file.txt", 'r') as f:
   print(f.read())
