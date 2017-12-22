#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


__app__ = "S02mqtt Adapter"
__VERSION__ = "0.85"
__DATE__ = "23.12.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'


import sys
import time
import json

from configobj import ConfigObj
from library.mqttpush import mqttpush
from library.logger import MyLogger
from library.S0Manager import S0manager

class manager(object):

    def __init__(self,cfg_file='S02mqtt.conf'):

        self._cfg_file = cfg_file

        self._cfg_broker = None
        self._cfg_log = None
        self._cfg_gpio = None


    def read_config(self):

        _cfg = ConfigObj(self._cfg_file)

        if bool(_cfg) is False:
            print('ERROR config file not found',self._cfg_file)
            sys.exit()
            #exit

        self._cfg_broker = _cfg.get('BROKER',None)
        self._cfg_log = _cfg.get('LOGGING',None)
        self._cfg_gpio = _cfg.get('GPIO',None)
        self._cfg_msgAdapter = _cfg.get('BROKER',None)
        return True

    def start_logger(self):
        self._log = MyLogger('S02MQTT')
        print(self._cfg_log)
        #self._log.handle(self._cfg_log.get('LOGMODE'),self._cfg_log)
        self._log.handle()
        self._log.level(self._cfg_log.get('LOGLEVEL','DEBUG'))
        return True

    def publishData(self,data):
        mqttc = mqttpush(self._mqttbroker)
        main_channel = self._mqttbroker.get('PUBLISH','/OPENHAB')

        for deviceId, measurement in data.items():
            channel = main_channel + '/' + deviceId
          #  print('channel',channel,deviceId)
            mqttc.publish(channel,measurement)

        return True

    def start_gpio(self):
      #  self.msgbus_subscribe
        self._log.debug('Start GPIO Interface with configuration: %s'% (self._cfg_gpio))
        self._S0mgr = S0manager(self._cfg_gpio,self.msgAdapter,self._log)
     #   self._gpio = gpio(self._cfg_gpio,'GPIO_SNK','GPIO_SRC','LOG')
        self._S0mgr.start()
        return True

    def msgAdapter(self,msg):
        #print('msg',msg)
        for deviceId, data in msg.items():
            self.publishData(deviceId,json.dumps(data))

        return True

    def publishData(self,deviceId,data):
        mqttc = mqttpush(self._cfg_broker)
        main_channel = self._cfg_broker.get('PUBLISH','/OPENHAB')

       # for deviceId, measurement in data.items():
        channel = main_channel + '/' + deviceId
          #  print('channel',channel,deviceId)
        self._log.debug('Push to mqtt server %s: %s'%(channel,deviceId))
        mqttc.publish(channel,data)

        return True

    def run(self):
        """
        Entry point, initiates components and loops forever...
        """
        self.read_config()
        self.start_logger()
        time.sleep(2)

        self._log.info('Startup, %s %s %s'% ( __app__, __VERSION__, __DATE__) )
        self.start_gpio()

       # while(True):
        #    if not self._S0mgr.isAlive():
         #       self._log.critical('%s died... restrart'%(__app__))
          #      self._S0mgr.__del__()
           #     self.start_gpio()

           # else:
            #    time.sleep(10)

if __name__ == "__main__":

    print ('main')
    if len(sys.argv) == 2:
        configfile = sys.argv[1]
    else:
    #    configfile = 'C:/Users/tgdscm41/PycharmProjects/Raspberry/S02mqtt1.cfg'
        configfile = 'C:/Users/tgdscm41/PycharmProjects/S02mqtt/S02mqtt1.cfg'
       # configfile = './S02mqtt1.cfg'
        #configfile =  '/home/pi/m2m/S02mqtt.cfg'

  #  print('Configfile',configfile)
    mgr_handle = manager(configfile)
    mgr_handle.run()