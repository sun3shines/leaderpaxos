# -*- coding: utf-8 -*-

import threading
from leaderpaxos.share.cache.lockdict import Mydict

SLEEP_INTERVAL = 1

def timer_func():
    wsgiObj.PAXOS_TIMER = threading.Timer(wsgiObj.PAXOS_LEADER_TERM**5,timer_func)

class pywsgi:
    def __init__(self):
        self.WSGI_CONF = '/usr/lib/python2.6/site-packages/leaderpaxos/acceptor/httpserver/core/paste.conf' 
        self.WSGI_SECT = 'server' 
        self.WSGI_HOST = None 
        self.WSGI_PORT = None 
        
        self.hostUuid = None        
        
        self.PAXOS_VALUE = Mydict()
        self.interruptEvent = threading.Event()
        
        self.PAXOS_LEADER_TERM = 20
        self.PAXOS_TIMER = threading.Timer(self.PAXOS_LEADER_TERM**5,timer_func)
        
        self.broadUuid = None
        
wsgiObj = pywsgi()
