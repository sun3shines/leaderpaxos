
import threading
from leaderpaxos.thread.proposer import paxos_state,display_state

class do_paxos_get_state(threading.Thread):
    def __init__(self,hostUuid=None,host=None,port=None):
        self.host = host
        self.port = port
        self.hostUuid = hostUuid
        threading.Thread.__init__(self)
        
    def run(self):
        paxos_state(self.host, self.port, self.hostUuid)
    
class do_paxos_display_state(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        display_state()
        
class do_paxos_communicate(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        pass