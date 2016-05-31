# -*- coding: utf-8 -*-

import threading
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import identiry_acceptor
from leaderpaxos.httpclient.libpaxos import paxos_broad
from leaderpaxos.thread.libtimer import paxos_timer_acceptor

def paxos_acceptor_main():
    
    wsgiObj.PAXOS_IDENTITY = identiry_acceptor
    
    while True:
        key,val = wsgiObj.PAXOS_QUEUE.get()
        start_time = val[1]
        wsgiObj.PAXOS_VALUE.put(key,val)
        threading.Timer(wsgiObj.PAXOS_LEADER_TERM,paxos_timer_acceptor,start_time).start()
        
def acceptor_broadcast(acceptorUuid,host,port):
    
    while True:
        
        wsgiObj.SIGNAL_SEND.get(acceptorUuid).get()
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        broadUuid = param.get('broadUuid')
        item = param.get('item')
        val = param.get('val')
        paxos_broad(host, port, item, val, broadUuid)

class do_paxos_acceptor(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        paxos_acceptor_main()
    
class do_acceptor_broad(threading.Thread):
    
    def __init__(self,acceptorUuid,host,port):
        
        threading.Thread.__init__(self)
        self.acceptorUuid = acceptorUuid
        self.host = host
        self.port = port
        
    def run(self):
        acceptor_broadcast(self.acceptorUuid, self.host, self.port)
    