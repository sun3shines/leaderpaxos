# -*- coding: utf-8 -*-

import threading
from leaderpaxos.acceptor.httpserver.static import wsgiObj as acceptorWsgiObj
from leaderpaxos.proposer.httpserver.static import wsgiObj as leaderWsgiObj
from leaderpaxos.share.urls import learn_paxos_leader,broad_paxos_leader
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid

def paxos_timer_acceptor():
    
    print 'acceptor timer reset leader information'
    acceptorWsgiObj.PAXOS_VALUE.put(learn_paxos_leader,acceptorWsgiObj.paxos_leader_default)
    acceptorWsgiObj.PAXOS_TIMER = threading.Timer(acceptorWsgiObj.PAXOS_LEADER_TERM,paxos_timer_acceptor)
    acceptorWsgiObj.PAXOS_TIMER.start()
    
def paxos_timer_leader():
    
    print 'leader timer reset leader information'
    leaderWsgiObj.LEADER_TIMER = threading.Timer(leaderWsgiObj.PAXOS_LEADER_TERM,paxos_timer_leader)
    leaderWsgiObj.LEADER_TIMER.start()
    broadUuid = get_broad_uuid()
    for hostUuid,_,_ in leaderWsgiObj.PAXOS_ACCEPTORS:
        leaderWsgiObj.CACHE_SEND.put(hostUuid,{'item':broad_paxos_leader,
                                         'val':(leaderWsgiObj.hostUuid,broadUuid)})
        leaderWsgiObj.SIGNAL_SEND.get(hostUuid).put(0)