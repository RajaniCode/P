import threading
import sys

class FailingThread(threading.Thread):
    def run(self):
        try:
            raise ValueError('x')
        except ValueError:
            self.exc_info = sys.exc_info()

failingThread = FailingThread()
failingThread.start()
failingThread.join()

print(failingThread.exc_info)
raise failingThread.exc_info[0], failingThread.exc_info[1], failingThread.exc_info[2] #
# Python 3.5
# raise failingThread.exc_info[0].with_traceback(failingThread.exc_info[1], failingThread.exc_info[2])

