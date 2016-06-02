# -*- coding: utf-8 -*-

import Queue
from statmachine.httpserver.static import wsgiObj

def machine_iduuid(hostuuid=None,host=None,port=None):
    
    wsgiObj.hostUuid = hostuuid
    wsgiObj.WSGI_HOST = host
    wsgiObj.WSGI_PORT = port
    
    def __deco(func):
        def _deco(*args,**kwargs):
            func(args,kwargs)
        return _deco                  
    return __deco


def create_queues():
    
    pass

def machine_load():
    
    create_queues()
    
    pass
