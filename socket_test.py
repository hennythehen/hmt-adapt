from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from socketIO_client import BaseNamespace
from socketIO_client import LoggingNamespace
from socketIO_client import SocketIO

def test(*args):
    print(args)

class Namespace(BaseNamespace):
    def on_tester(self, *args):
        print('test: ', args)

socketio = SocketIO('http://ec2-52-24-126-225.us-west-2.compute.amazonaws.com', 81, LoggingNamespace)
io = socketio.define(Namespace, '/socket.io')

io.emit('testee', 'hello')
socketio.wait(seconds=1)

