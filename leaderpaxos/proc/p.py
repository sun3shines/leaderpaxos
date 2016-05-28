
import os
import os.path
from leaderpaxos.httpserver.core.static import wsgiObj

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

