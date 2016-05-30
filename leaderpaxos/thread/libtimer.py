# -*- coding: utf-8 -*-

import threading
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import learn_paxos_leader

def paxos_timer_acceptor():
    
    print 'acceptor timer reset leader information'
    wsgiObj.PAXOS_VALUE.put(learn_paxos_leader,('',0))
    wsgiObj.PAXOS_TIMER = threading.Timer(wsgiObj.PAXOS_LEADER_TERM,paxos_timer_acceptor)
    wsgiObj.PAXOS_TIMER.start()