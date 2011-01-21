import entangled.dtuple
import time
from twisted.internet import reactor, defer
import base64
import hashlib
import sys
from bottle import route, run, debug
import threading
from bottle import static_file
import json

getResult = []
debug(True)

def printError(result):
  print result

def _tupleFromStr(text):
    tp = None
    try:
        exec 'tp = %s' % text
        if type(tp) != tuple:
            raise Exception
    except Exception:
        dialog = gtk.MessageDialog(self, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                    "Please enter a valid Python tuple,\ne.g. (1, 'abc', 3.14)")
        dialog.set_title('Error')
        dialog.run()
        dialog.destroy()
    finally:
        return tp

def completed(result):
  print "done"
  print result

def readStuff(command,block,color):
  
  def showValue(result,x):
    global getResult
    h = hashlib.sha1()
    h.update(str(x))
    hKey = h.digest()
    blockResult = result[hKey]
    getResult.append({"number":x,"result":blockResult})

  if command == "set":
    node.publishData(block, color)
    
  else:
    for x in range(4999):
      key = str(x)
      h = hashlib.sha1()
      h.update(key)
      hKey = h.digest()
      df = node.iterativeFindValue(hKey)
      df.addCallback(showValue,x)
    

@route('/:filename')
def server_static(filename):
    return static_file(filename, root='/home/tyler/entangled-0.1/public')  
    
@route('/blocks')
def blocks():
    readStuff("get",None, None)
    time.sleep(5)
    print getResult
    return json.dumps(getResult)
  
@route('/set/:block/:color')
def set(block,color):
  readStuff("set",block.title(),color.title())
  return block.title() + " " + color.title()


class reactive(threading.Thread):
  def run(self):
    print "starting reactor"
    run(host='localhost', port=8080)


reactive().start()
print "and other stuff..."   
node = entangled.dtuple.DistributedTupleSpacePeer(3000)
node.joinNetwork([("127.0.0.1",int(4000))])
reactor.run()






