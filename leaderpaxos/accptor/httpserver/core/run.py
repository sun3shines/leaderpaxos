# -*- coding: utf-8 -*-

import traceback
from leaderpaxos.accptor.httpserver.static import wsgiObj
from leaderpaxos.accptor.httpserver.core.wsgi import run_wsgi

def start():
    wsgiObj.interruptEvent.clear()
    try:
        run_wsgi(wsgiObj.WSGI_CONF, wsgiObj.WSGI_SECT, 
                 wsgiObj.WSGI_HOST,wsgiObj.WSGI_PORT)
    except:
        print traceback.format_exc()
        wsgiObj.interruptEvent.set()
        