# -*- coding: utf-8 -*-

from leaderpaxos.httpserver.core.static import wsgiObj
from leaderpaxos.httpserver.core.wsgi import run_wsgi

def start():

    run_wsgi(wsgiObj.WSGI_CONF, wsgiObj.WSGI_SECT, 
             wsgiObj.WSGI_HOST,wsgiObj.WSGI_PORT)
    
