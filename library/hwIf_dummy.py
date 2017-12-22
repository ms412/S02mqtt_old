
import time
import random
from threading import Thread

class dummy(Thread):

    def __init__(self,logChannel):
        Thread.__init__(self)

        self._log = logChannel
        self._callback = None

    def Reset(self):
        return True

    def ConfigIO(self,ioPin,iodir,pullup=None):
        return True

    def WritePin(self,ioPin,value):
        return True

    def ReadPin(self,ioPin):
        value = random.choice([True, False])
        return value

    def Edge(self,ioPin,callback,trigger,debounce=100):
        print('GPIO Edge',ioPin, callback, trigger, debounce)
        self._pin = ioPin
        self._callback = callback
        self.start()
        return True


    def run(self):
        while True:
            time.sleep(10)

            #print('#')
            value = random.choice([True, False])
            self._callback(self._pin)