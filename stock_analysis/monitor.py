import threading
import random
import time
import sys

class MonitorThread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.threadEvent = event

    def run(self):
        print ('Monitor is ready.\n')
        while True:
            if self.threadEvent.isSet():
                print ('Monitor is running...\n')
                time.sleep(.1)
            else:
                print ('Monitor is stopped.\n')
                break

def main():
    count = 60
    cnf = 0
    event = threading.Event()
    while count >= 0:
        print ('There are %s tasks in queue!' % str(cnf))
        count -= 1
        num = random.randint(1, 100)
        if num%5 == 0:
            if cnf == 0:
                event.set()
                t = MonitorThread(event)
                t.start()
            cnf += 1
        elif num%3 == 0 and num%15 != 0:
            if cnf >= 1:
                event.clear()
                time.sleep(2)
            if cnf >= 1:
                cnf -= 1
    time.sleep(5)
    if cnf >= 1:
        event.clear()

if __name__ == '__main__':
    sys.exit(main())