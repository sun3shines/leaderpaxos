# -*- coding: utf-8 -*-

import Queue
from statmachine.httpserver.static import wsgiObj

def machine_iduuid(leaderInfo =None):
    
    
    wsgiObj.WSGI_HOST = '127.0.0.1'
    wsgiObj.WSGI_PORT = 18000
    
    wsgiObj.leaderUuid ,wsgiObj.leaderHost ,wsgiObj.leaderPort = leaderInfo
    
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
