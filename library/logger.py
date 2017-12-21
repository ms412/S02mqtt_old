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


__app__ = "loghandler"
__VERSION__ = "0.8"
__DATE__ = "09.07.2017"
__author__ = "Markus Schiesser"
__contact__ = "M.Schiesser@gmail.com"
__copyright__ = "Copyright (C) 2017 Markus Schiesser"
__license__ = 'GPL v3'


import logging
import logging.handlers
import socket

class logger:
    instance = None
    def __init__(self,log = None):
        if not logger.instance:
            logger.instance = logger.__logger()
        else:
            logger.instance.val = log

    def __getattr__(self, item):
        return getattr(self.instance, item)

    class __logger(object):

        def __init__(self,name = None):

            self._loghandle = ''

            self._logger = logging.getLogger(name)
            self._logger.setLevel(logging.DEBUG)

        def level(self,level):
            if level in 'INFO':
                self._logger.setLevel(logging.INFO)
            elif level in 'DEBUG':
                self._logger.setLevel(logging.DEBUG)
            return True

        def handle(self,method = 'PRINT',config = None):
         #   print (methode)
            if 'SYSLOG' in method:
              #  print('Ssyslog',config )
                host = config.get('LOGSERVER','localhost')
               # print('Syslog',host)
                handler = logging.handlers.SysLogHandler(address=(host, 514), facility=19)

                hostname = socket.gethostname()
                formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s %(message)s'.format(hostname),'%b %e %H:%M:%S')
                handler.setFormatter(formatter)

            elif 'LOGFILE' in method:
                file = config.get('LOGFILE','./logger.log')
                handler = logging.FileHandler(file)
                formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s','%b %e %H:%M:%S')
                handler.setFormatter(formatter)

            else:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%b %e %H:%M:%S')
                handler.setFormatter(formatter)


            self._logger.addHandler(handler)

            return True


        def log(self,level, *argv):
            print('LOG',level,argv)
            if 'DEBUG' in level:
                self._logger.debug(argv)
            elif 'ERROR' in level:
                self._logger.error(argv)
            elif'CRITICAL' in level:
                self._logger.critical(argv)
            elif 'WARNING' in level:
                self._logger.warning(argv)
            else:
                self._logger.info(argv)


        def debug(self,msg):
        #    print('debug',msg)
            self._logger.debug(msg)

        def info(self,msg):
         #   print('info',msg)
            self._logger.info(msg)

        def warning(self,msg):
          #  print('warning',msg)
            self._logger.warning(msg)

        def error(self,msg):
           # print('error',msg)
            self._logger.error(msg)

        def critical(self,msg):
           # print('critical',msg)
            self._logger.critical(msg)


    class dummylog(object):
        def debug(self, msg):
            print('DEBUG',msg)

        def info(self, msg):
            print('INFO',msg)

        def warning(self, msg):
            print('WARNING',msg)

        def error(self, msg):
            print('ERROR',msg)

        def critical(self, msg):
            print('CRITICAL',msg)

class app(object):

    def __init__(self,log):
        self._log = log
        self._log.info('start')

    def methode(self, x):
        msg = 'test' + x
        self._log.debug(msg)


if __name__ == '__main__':
    log = logger('TEST')
    log.handle('SYSLOG',{'HOST':'172.17.115.121'})
    log.info('TEST')
    appX = app(log)
    appX.methode('iii')