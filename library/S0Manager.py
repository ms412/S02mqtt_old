
import sys
import time
import threading


'''
import device interface drivers
'''
from library.logger import MyLogger
#from library.hwIf_raspberry import raspberry
from library.hwIf_dummy import dummy
from library.tempfile import tempfile
from library.S0Gas import S0Gas

class S0manager(threading.Thread):

    def __init__(self,config,callback,logChannel):
        threading.Thread.__init__(self)


        self._cfg = config
        self._callback = callback
        self._log = MyLogger()
      #  self._tempdir = str(config.get('TEMPDIR','./'))
        self._tmpfilename = str(config.get('TEMPFILE','S02mqtt.temp'))
        self._update = int(self._cfg.get('UPDATE',60))

        '''
        Hardware handel stores the handle to the hardware
        only once available per VDM instance
        '''
        self._tempFile = None
        self._hwHandle = None
        self._devHandle = {}

        self.msg = {}

        self._log.debug('S0manager %s'%config)

        self.setup()

    def __del__(self):
        self._log.debug('S0manager kill my self')
       # print('kill myself')


    def setup(self):
        self._tempFile = tempfile(self._tmpfilename)
        tmpdata = self._tempFile.openfile()

        if tmpdata == None:
          #  print('file does not exist')
           # log_msg = 'Tempfile does not exist'
            self._log.info('Tempfile does not exist: %s'% self._tmpfilename)
        else:
            #print('Data',tmpdata)
            #log_msg =
            self._log.info('Tempfile exit read old values')

 #       if 'RASPBERRY' in self._cfg.get('HWIF','RASPBERRY'):
  #          self._hwHandle = raspberry(self._log)
   #     elif 'DUMMY'in self._cfg.get('HWIF','RASPBERRY'):
    #        self._hwHandle = dummy(self._log)
     #   else:
      #      self._log.critical('HWInterface %s unknown'% self._cfg.get('HWIF',None))
       #     sys.exit()

        for _pin, _cfg in self._cfg.items():
        #    print(_pin, _cfg)
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

                if 'RASPBERRY' in _cfg.get('HWIF', 'RASPBERRY'):
                    self._hwHandle = raspberry(self._log)
                elif 'DUMMY' in _cfg.get('HWIF', 'RASPBERRY'):
                    self._hwHandle = dummy(self._log)
                else:
                    self._log.critical('HWInterface %s unknown' % _cfg.get('HWIF', None))
                    sys.exit()

                #self._devHandle[_pin] = S0(self._hwHandle, _pin, _cfg, self._log)
                self._devHandle[_pin] = S0Gas(self._hwHandle, _cfg)

        return True

    def run(self):

        #print('Start Thread')
        _timeout = time.time() + self._update

        while True:
#            time.sleep(0.3)

           # print('time',_timeout, time.time())
            if time.time() > _timeout:
            #    print('Send update')
                self._log.info('Timer expired get update')
#             #   self.msgbus_publish(self._log, '%s %s: %s ' % ('DEBUG', self.whoami(), log_msg))

                for key,value in self._devHandle.items():
               #     print('Update',key,value)
                    self.msg[key]=value.getData()
                #    self._tempFile.writefile(self.msg)

                self._callback(self.msg)


                self._tempFile.writefile(self.msg)
         #       print('power',self.msg)
              #  self._log.debug('Send Update %s'% self.msg)

                _timeout = time.time() + self._update

        return True

