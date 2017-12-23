
import time


'''
import device interface drivers
'''
from library.logger import MyLogger
#from library.hwIf_raspberry import raspberry
#from library.hwIf_dummy import dummy
#from library.tempfile import tempfile




class S0Gas(object):

    def __init__(self,hwHandle,cfg):
      #  Thread.__init__(self)

        self._hwHandle = hwHandle
       # self._callback = callback
        self._cfg = cfg
        self._log = MyLogger()

        '''
        System parameter
        '''
      #  self._log.debug('Startup s%'% self._cfg)
        self._pin = int(self._cfg.get('GPIO',None))
        self._factor = int(self._cfg.get('FACTOR',1000))
        self._accuracyWatt = int(self._cfg.get('ACCURACY',360))
        self._attenuator = str(self._cfg.get('ATTENUATOR','UP'))
        self._trigger = str(self._cfg.get('TRIGGER','RISING'))
        self._debounce = int(self._cfg.get('DEBOUNCE',100))
       # self._power = float(self._cfg.get('POWER',0))
        #self._energy = float(self._cfg.get('ENERGY',0))

        '''
        Class variables
        '''
        self._pulsCounter = self._cfg.get('PULS_SUMME',0)
        self._timeCounter = self._cfg.get('TIME_SUMME',0)
        self._pulsDelta  = self._cfg.get('PULS_DELTA',0)
        self._timeDelta = self._cfg.get('TIME_DELTA',0)

        self._T0 = 0
        self._timeDelta = 0
        self._pulsDelta = 0

        self.setup()

    def setup(self):

        self._T0 = time.time()

        if not self._pin == None:
            self._hwHandle.ConfigIO(self._pin,'IN',self._attenuator)
            self._hwHandle.Edge(self._pin,self.callback,self._trigger,self._debounce)

        return True

    def callback(self,pin):
        #print('callback',pin)

        if self._pulsCounter > 0:

         #   print('%s Test'% pin)
            _timeCurrent = time.time()
            _T1 = _timeCurrent - self._T0
            self._timeDelta = self._timeDelta + _T1
            self._timeCounter = self._timeCounter + _T1
            self._pulsDelta = self._pulsDelta + 1

            self._T0 = _timeCurrent

        else:
            _timeCurrent = time.time()
            _T1 = _timeCurrent - self._T0
            self._log.debug('%s First Puls now Start'% pin)
            self._pulsCounter = self._pulsCounter + 1
        #    self._pulsDelta = self._pulsDelta + 1
         #   self._timeDelta = self._timeDelta + _T1
            self._timeCounter = self._timeCounter + _T1


        return True

    def getData(self):
        data = {}
        data['PULS_SUMME'] = self._pulsCounter
        data['PULS_DELTA'] = self._pulsDelta
        data['TIME_SUMME'] = self._timeCounter
        data['TIME_DELTA'] = self._timeDelta

        self._timeDelta = 0
        self._pulsDelta = 0
        return data
