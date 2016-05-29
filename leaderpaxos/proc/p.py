
import os
import os.path
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.thread.libthread import do_paxos_get_state,do_paxos_display_state
def iduuid(hostuuid=None,host=None,port=None,hosts=[]):
    wsgiObj.hostUuid = hostuuid
    wsgiObj.WSGI_HOST = host
    wsgiObj.WSGI_PORT = port
    wsgiObj.PAXOS_HOSTS = hosts

    def __deco(func):
        def _deco(*args,**kwargs):
            func(args,kwargs)
        return _deco	          	
    return __deco

def load():
    workdir = '/'.join(['/home','paxos',wsgiObj.hostUuid])
    print workdir
    if not os.path.exists(workdir):
        os.mkdir(workdir)
        
    for hostUuid,host,port in wsgiObj.PAXOS_HOSTS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        do_paxos_get_state(hostUuid,host,port).start()
        
    do_paxos_display_state().start()
    
