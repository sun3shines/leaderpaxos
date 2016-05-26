# -*- coding: utf-8 -*-

import leaderpaxos.wsgi.static
from leaderpaxos.wsgi.wsgi import run_wsgi

def start():

    print leaderpaxos.wsgi.static.PROC_HOST,leaderpaxos.wsgi.static.PROC_PORT
    
    run_wsgi(leaderpaxos.wsgi.static.PROC_PASTE_CONF, 
             leaderpaxos.wsgi.static.PROC_PASTE_APP_SECTION, 
             leaderpaxos.wsgi.static.PROC_HOST,
             leaderpaxos.wsgi.static.PROC_PORT)
    
if __name__ == '__main__':
    start()
    
