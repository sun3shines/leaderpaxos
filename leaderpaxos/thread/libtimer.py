# -*- coding: utf-8 -*-

import threading
from leaderpaxos.acceptor.httpserver.static import wsgiObj as acceptorWsgiObj
from leaderpaxos.proposer.httpserver.static import wsgiObj as leaderWsgiObj
from leaderpaxos.share.urls import learn_paxos_leader
from leaderpaxos.thread.communicate import paxos_broad_leader

def paxos_timer_acceptor():
    
    print 'acceptor timer reset leader information'
    acceptorWsgiObj.PAXOS_VALUE.put(learn_paxos_leader,acceptorWsgiObj.paxos_leader_default)
    acceptorWsgiObj.PAXOS_TIMER = threading.Timer(acceptorWsgiObj.PAXOS_LEADER_TERM,paxos_timer_acceptor)
    acceptorWsgiObj.PAXOS_TIMER.start()
    
def paxos_timer_leader():
    
    print 'leader timer reset leader information'
    leaderWsgiObj.LEADER_TIMER = threading.Timer(leaderWsgiObj.PAXOS_LEADER_TERM,paxos_timer_leader)
    leaderWsgiObj.LEADER_TIMER.start()
    paxos_broad_leader()