# -*- coding: utf-8 -*-

from leaderpaxos.acceptor.httpserver.static import wsgiObj as acceptorWsgiObj
from leaderpaxos.share.urls import learn_paxos_leader

def paxos_timer_acceptor(start_time):
    
    val = acceptorWsgiObj.PAXOS_VALUE.get(learn_paxos_leader)
    current_time = val[1]
    if current_time > start_time:
        pass
    else:
        print 'timeout,acceptor timer reset leader information'
        acceptorWsgiObj.PAXOS_VALUE.put(learn_paxos_leader,acceptorWsgiObj.paxos_leader_default)
    