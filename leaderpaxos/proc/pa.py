

from leaderpaxos.acceptor.httpserver.static import wsgiObj

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


    
