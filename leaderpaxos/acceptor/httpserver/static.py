# -*- coding: utf-8 -*-

import Queue
import threading
from leaderpaxos.share.cache.lockdict import Mydict

class pywsgi:
    def __init__(self):
        self.WSGI_CONF = '/usr/lib/python2.6/site-packages/leaderpaxos/acceptor/httpserver/core/paste.conf' 
        self.WSGI_SECT = 'server' 
        self.WSGI_HOST = None 
        self.WSGI_PORT = None 
        
        self.hostUuid = None        
        
        self.PAXOS_VALUE = Mydict()
        self.PAXOS_QUEUE = Queue.Queue()
        
        self.interruptEvent = threading.Event()
        
        self.PAXOS_LEADER_TERM = 20
        
        self.broadUuid = None 
        
        self.paxos_leader_default = ('',0,'')
        
        self.PAXOS_IDENTITY = None
        
        self.SIGNAL_BROAD_SEND = Mydict()
        
        self.CACHE_BROAD_SEND = Mydict()
        
        self.PAXOS_ACCEPTORS = []
        
        self.itemBroadUuid = Mydict()
        
wsgiObj = pywsgi()
