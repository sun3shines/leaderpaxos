# -*- coding: utf-8 -*-

import Queue
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.thread.acceptor import do_acceptor_broad,do_paxos_acceptor

def acceptor_iduuid(hostuuid=None,host=None,port=None,acceptors=[]):
    
    wsgiObj.hostUuid = hostuuid
    wsgiObj.WSGI_HOST = host
    wsgiObj.WSGI_PORT = port
    
    wsgiObj.PAXOS_ACCEPTORS = acceptors
    
    def __deco(func):
        def _deco(*args,**kwargs):
            func(args,kwargs)
        return _deco                  
    return __deco


def create_queues():
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.SIGNAL_SEND.put(hostUuid,Queue.Queue())
    pass

def acceptor_load():
    
    create_queues()
    
    for acceptorUuid,host,port in wsgiObj.PAXOS_ACCEPTORS:
        if acceptorUuid == wsgiObj.hostUuid:
            continue
        do_acceptor_broad(acceptorUuid,host,port).start()
        
    do_paxos_acceptor().start()
    