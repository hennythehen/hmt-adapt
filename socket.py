from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO

def test(*args):
    print(args)


socketio = SocketIO('localhost', 5000, LoggingNamespace)
socketio.on('tester', test)
socketio.emit('testee', 'asdf')
socketio.wait(seconds=1)
