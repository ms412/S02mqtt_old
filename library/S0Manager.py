#import json
#import time
import sys

from threading import Thread
#from threading import Event
#from queue import Queue
import time


'''
import device interface drivers
'''

from library.hwIf_raspberry import raspberry
from library.hwIf_dummy import dummy
from library.tempfile import tempfile

class S0manager(Thread):

    def __init__(self,config,callback,logChannel):
        Thread.__init__(self)

        self._cfg = config
        self._callback = callback
        self._log = logChannel
        self._tmpfilename = str(self._cfg.get('TEMPFILE','S02mqtt.temp'))
        self._update = int(self._cfg.get('UPDATE',60))

        '''
        Hardware handel stores the handle to the hardware
        only once available per VDM instance
        '''
        self._hwHandle = None
        self._devHandle = {}

        self.msg = {}

        self.setup()

    def __del__(self):
        self._log.debug('S0manager kill my self')


    def setup(self):
        self._tempFile = tempfile(self._tmpfilename, self._log)
        tmpdata = self._tempFile.openfile()

        if tmpdata == None:
          #  print('file does not exist')
            log_msg = 'Tempfile does not exist'
            self._log.info('Tempfile does not exist: %s'% self._tmpfilename)
        else:
            #print('Data',tmpdata)
            #log_msg =
            self._log.info('Tempfile exit read old values')

        if 'RASPBERRY' in self._cfg.get('HWIF','RASPBERRY'):
            self._hwHandle = raspberry(self._log)
        elif 'DUMMY'in self._cfg.get('HWIF','RASPBERRY'):
            self._hwHandle = dummy(self._log)
        else:
            self._log.critical('HWInterface %s unknown'% self._cfg.get('HWIF',None))
            sys.exit()

        for _pin, _cfg in self._cfg.items():
            print(_pin, _cfg)
            if isinstance(_cfg, dict):
                if tmpdata != None:
                    _tmp = tmpdata.get(_pin,None)
                   # print('Temp',_tmp,_pin,tmpdata.get('ENERGY',0))
                    if None == _tmp:
                        _cfg['TIME_SUMME'] = 0
                        _cfg['TIME_DELTA'] = 0
                        _cfg['PULS_SUMME'] = 0
                    else:
                        _cfg['TIME_SUMME'] = _tmp.get('TIME_SUMME',0)
                        _cfg['TIME_DELTA'] = _tmp.get('TIME_DELTA',0)
                        _cfg['PULS_SUMME'] = _tmp.get('PULS_SUMME', 0)
           #        _cfg['TIME'] = _tmp.get('TIME',0)

                #self._devHandle[_pin] = S0(self._hwHandle, _pin, _cfg, self._log)
                self._devHandle[_pin] = S0(self._hwHandle, _cfg, self._log)
              #  print('devHandle',self._devHandle)
        return True

    def run(self):

        _timeout = time.time() + self._update


        while True:
#            time.sleep(0.3)

            if time.time() > _timeout:
              #  print('Send update')
                self._log.info('Timer expired get update')
#                self.msgbus_publish(self._log, '%s %s: %s ' % ('DEBUG', self.whoami(), log_msg))

                for key,value in self._devHandle.items():
          #         print('.',key,value)
                    self.msg[key]=value.getData()
                    self._tempFile.writefile(self.msg)
                    self._callback(self.msg)

              #  print('power',self.msg)
                self._log.debug('Send Update %s'% self.msg)

                _timeout = time.time() + self._update

        return True

class S0(object):

    def __init__(self,hwHandle,cfg,logChannel):

        self._hwHandle = hwHandle
        self._cfg = cfg
        self._log = logChannel

        '''
        System parameter
        '''
        print('Startup',self._cfg)
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
       # self._powerData = []
        #self._t_update = 0
        self._pulsCounter = self._cfg.get('PULS_SUMME',0)
        self._timeCounter = self._cfg.get('TIME_SUMME',0)

        self._T0 = 0
        self._Tdelta = 0
        self._Pdelta = 0

        self.setup()

    def setup(self):

      #  self._powerData.append(self._power)
       # self._pulsSum =
        self._T0 = time.time()



   #     self._accuracySec = 3600 * 1000 / self._factor / self._accuracyWatt

        if not self._pin == None:
            self._hwHandle.ConfigIO(self._pin,'IN',self._attenuator)
            self._hwHandle.Edge(self._pin,self.callback,self._trigger,self._debounce)

        return True

    def callback(self,pin):
     #   print('callback',pin)
        self._log.debug('Callback from Pin: %s'% pin)

        if self._pulsCounter > 0:

        #    print('Test',self._t_update,self._powerData)

            _timeCurrent = time.time()
            _T1 = _timeCurrent - self._T0
            self._Tdelta = self._Tdelta + _T1
            self._timeCounter = self._timeCounter + _T1
            self._Pdelta = self._Pdelta + 1

            #self._powerData.append(self.power(self._t_update,_timeCurrent))
           # self._Tdelta = _timeCurrent - self._T0
         #   self._timeCounter = self._timeCounter + self._Tdelta
           # print('Conter',self._timeCounter,self._Tdelta,self._pulsCounter)
            self._log.debug('Pin: %s, Total Time Counter: %s, Time Delta: %s, Total Puls Counter: %s, Puls Delta: %s' % (pin,self._timeCounter, self._Tdelta,self._pulsCounter,self._Pdelta))

            #self._t_update = _timeCurrent
            self._T0 = _timeCurrent

        else:
        #    print('First Puls now Start')
            self._log.debug('Start Counter Pin: %s'% pin)

        self._pulsCounter = self._pulsCounter + 1

      #  print('callback',self._powerData)
        return True

    def getData(self):
        data = {}
        data['PULS_SUMME'] = self._pulsCounter
        data['PULS_DELTA'] = self._Pdelta
        data['TIME_SUMME'] = self._timeCounter
        data['TIME_DELTA'] = self._Tdelta

        self._Tdelta = 0
        self._Pdelta = 0
        return data
