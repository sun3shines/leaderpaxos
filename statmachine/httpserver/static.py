# -*- coding: utf-8 -*-

import Queue
import threading
from leaderpaxos.share.cache.lockdict import Mydict

class pywsgi:
    def __init__(self):
        self.WSGI_CONF = '/usr/lib/python2.6/site-packages/statmachine/httpserver/core/paste.conf' 
        self.WSGI_SECT = 'server' 
        self.WSGI_HOST = None 
        self.WSGI_PORT = None 
            
        self.interruptEvent = threading.Event()

        self.MACHINE_STATE = Mydict()
        
        self.leaderUuid = None
        self.leaderHost = None
        self.leaderPort = None
        
wsgiObj = pywsgi()
