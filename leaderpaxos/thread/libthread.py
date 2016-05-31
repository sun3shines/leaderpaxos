# -*- coding: utf-8 -*-

import threading
from leaderpaxos.thread.proposer import paxos_state,display_state,paxos_broad_base,\
    paxos_decision,paxos_proposer_main,paxos_learn_base

class do_paxos_get_state(threading.Thread):
    def __init__(self,hostUuid=None,host=None,port=None):
        self.host = host
        self.port = port
        self.hostUuid = hostUuid
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            paxos_state(self.host, self.port, self.hostUuid)
        except:
            pass
    
class do_paxos_display_state(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            display_state()
        except:
            pass
        
class do_paxos_learn(threading.Thread):
    
    def __init__(self,acceptorUuid,host,port):
        threading.Thread.__init__(self)
        self.acceptorUuid = acceptorUuid
        self.host = host
        self.port = port
        
    def run(self):
        try:
            paxos_learn_base(self.acceptorUuid, self.host, self.port)
        except:
            pass
    
class do_paxos_broad(threading.Thread):
    
    def __init__(self,acceptorUuid,host,port):
        threading.Thread.__init__(self)
        self.acceptorUuid = acceptorUuid
        self.host = host
        self.port = port
        
    def run(self):
        try:
            paxos_broad_base(self.acceptorUuid, self.host, self.port)
        except:
            pass
        
class do_paxos_decision(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            paxos_decision()
        except:
            pass
    
class do_paxos_proposer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            paxos_proposer_main()
        except:
            pass

    