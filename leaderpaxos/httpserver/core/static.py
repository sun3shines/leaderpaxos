
class pywsgi:
    def __init__(self):
        self.WSGI_CONF = '/usr/lib/python2.6/site-packages/leaderpaxos/httpserver/core/paste.conf' 
        self.WSGI_SECT = 'server' 
        self.WSGI_HOST = None 
        self.WSGI_PORT = None 
        self.hostUuid = None        
        self.PAXOS_HOSTS = []

wsgiObj = pywsgi()
