import json
import os

class tempfile(object):

    def __init__(self,filename):

        self._filename = filename

    def openfile(self):

        try:
            with open(self._filename)as fh:
                data = json.load(fh)
            #    print('test',data)
                fh.close()

        except IOError:
            data = None

        return data

    def writefile(self,data):
        _jdata= json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
       # filepath = os.path.join(self._path, filename)
        f = open(self._filename,"w")
        f.write(_jdata)
        f.close()
           # with open(self._filename,'w')as fh:

 #   def writefile(self,filename):
       # filepath = os.path.join(self._path, filename)
  #      f = open(self._filename,"a")
   #     f.close()
           # with open(self._filename,'w')as fh:


