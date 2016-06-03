# -*- coding: utf-8 -*-

import os
import os.path
import Queue
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.thread.libthread import do_paxos_get_state,do_paxos_display_state,\
    do_paxos_broad,do_paxos_learn,do_paxos_decision,do_paxos_proposer
from leaderpaxos.share.signal import signal_sleep

def proposer_iduuid(index,hostuuid=None,host=None,port=None,
                    hosts=[],acceptors=[],mst_cmd=''):
    
    wsgiObj.procindex = index
    wsgiObj.hostUuid = hostuuid
    wsgiObj.WSGI_HOST = host
    wsgiObj.WSGI_PORT = port
    wsgiObj.PAXOS_HOSTS = hosts
    wsgiObj.PAXOS_ACCEPTORS = acceptors
    wsgiObj.mst_cmd = mst_cmd
    
    def __deco(func):
        def _deco(*args,**kwargs):
            func(args,kwargs)
        return _deco	          	
    return __deco

def create_queues():
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.SIGNAL_LEARN_SEND.put(hostUuid,Queue.Queue())
        wsgiObj.SIGNAL_BROAD_SEND.put(hostUuid,Queue.Queue())

def proposer_load():
    
    workdir = '/'.join(['/home','paxos',wsgiObj.hostUuid])
    print workdir
    if not os.path.exists(workdir):
        os.mkdir(workdir)

    for hostUuid,host,port in wsgiObj.PAXOS_HOSTS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        do_paxos_get_state(hostUuid,host,port).start()
        
    do_paxos_display_state().start()
    
    create_queues()
    
    for acceptorUuid,host,port in wsgiObj.PAXOS_ACCEPTORS:
        if acceptorUuid == wsgiObj.hostUuid:
            continue
        do_paxos_broad(acceptorUuid,host,port).start()
        do_paxos_learn(acceptorUuid,host,port).start()
       
    do_paxos_decision().start()
    do_paxos_proposer().start()
