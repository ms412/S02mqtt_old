import os
#import library.libpaho as mqtt
import paho.mqtt.client as mqtt



class mqttpush(object):

    def __init__(self,config):
        '''
        setup mqtt broker
        config = dictionary with configuration
        '''

        self._config = config

        '''
        create mqtt session
        '''
        #self.create()
        self._mqttc = mqtt.Client(str(os.getpid()),clean_session=True)

        self._host = str(self._config.get('HOST','localhost'))
        self._port = int(self._config.get('PORT',1883))
        self._user = str(self._config.get('USER',None))
        self._password = str(self._config.get('PASSWD',None))
        self._publish = str(self._config.get('PUBLISH','/PUBLISH'))

    def publish(self,channel,payload):
        _channel = self._publish + '/' + channel
        self._mqttc.connect(self._host)
        self._mqttc.publish(_channel,payload)
       # print('cc',channel,msg)
        self._mqttc.loop(2)
        self._mqttc.disconnect()
        return True
