# -*- coding: utf-8 -*-

import threading
import traceback

from leaderpaxos.thread.alive import display_state,paxos_state
from leaderpaxos.thread.proposer import paxos_decision,paxos_proposer_main
from leaderpaxos.thread.learn import paxos_learn_base
from leaderpaxos.thread.broad import paxos_broad_base

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
            print 'thread down do_paxos_get_state'
            pass
    
class do_paxos_display_state(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            display_state()
        except:
            print 'thread down do_paxos_display_state'
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
            print 'thread down do_paxos_learn'
            print traceback.format_exc()
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
            print 'thread down do_paxos_broad'
            print traceback.format_exc()
            pass
        
class do_paxos_decision(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            paxos_decision()
        except:
            print 'thread down do_paxos_decision'
            pass
    
class do_paxos_proposer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            paxos_proposer_main()
        except:
            print traceback.format_exc()
            print 'thread down do_paxos_proposer'
            pass

    
