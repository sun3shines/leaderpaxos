
import os
import os.path
import Queue
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.thread.libthread import do_paxos_get_state,do_paxos_display_state

def proposer_iduuid(hostuuid=None,host=None,port=None,hosts=[],acceptors=[]):
    
    wsgiObj.hostUuid = hostuuid
    wsgiObj.WSGI_HOST = host
    wsgiObj.WSGI_PORT = port
    wsgiObj.PAXOS_HOSTS = hosts
    wsgiObj.PAXOS_ACCEPTORS = acceptors
    
    def __deco(func):
        def _deco(*args,**kwargs):
            func(args,kwargs)
        return _deco	          	
    return __deco

def create_queues():
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        wsgiObj.SIGNAL_SEND.put(hostUuid,Queue.Queue())
    pass

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
    
