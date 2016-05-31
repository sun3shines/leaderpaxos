# -*- coding: utf-8 -*-

import Queue
import threading
from leaderpaxos.share.cache.lockdict import Mydict

def timer_func():
    wsgiObj.LEADER_TIMER = threading.Timer(wsgiObj.PAXOS_LEADER_TERM**5,timer_func)

class pywsgi:
    def __init__(self):
        
        self.WSGI_CONF = '/usr/lib/python2.6/site-packages/leaderpaxos/proposer/httpserver/core/paste.conf' 
        self.WSGI_SECT = 'server' 
        self.WSGI_HOST = None 
        self.WSGI_PORT = None 
        self.hostUuid = None       
         
        self.PAXOS_HOSTS = []
        self.PAXOS_ACCEPTORS = []
        
        self.PAXOS_STATE = Mydict()
        self.interruptEvent = threading.Event()
        
        self.SIGNAL_LEARN_SEND = Mydict()
        self.SIGNAL_LEARN_RECV = Queue.Queue()

        self.SIGNAL_BROAD_SEND = Mydict()
        
        self.CACHE_SEND = Mydict()
        self.CACHE_RECV = Mydict()
        
        self.PAXOS_IDENTITY = None
        
        self.MAIN_LEARN_RECV = Queue.Queue()
        
        self.PAXOS_LEADER_TERM = 20
         
        self.broadUuid = None
        self.leaderUuid = None
        
        self.PAXOS_TRY_TERM = 2
        
        self.LEADER_TIMER = threading.Timer(self.PAXOS_LEADER_TERM**5,timer_func)
        self.paxos_leader_default = ('',0,'')
        
wsgiObj = pywsgi()
