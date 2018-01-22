from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import httplib
import websocket

def connect(self) :
    conn  = httplib.HTTPConnection('localhost:8124')
    conn.request('POST','/socket.io/1/')
    resp  = conn.getresponse()
    hskey = resp.read().split(':')[0]

    self._ws = websocket.WebSocket(
                    'ws://localhost:8000/socket.io' + hskey,
                    onopen   = self._onopen,
                    onmessage = self._onmessage)