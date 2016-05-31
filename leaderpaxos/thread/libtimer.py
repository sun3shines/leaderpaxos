# -*- coding: utf-8 -*-

from leaderpaxos.acceptor.httpserver.static import wsgiObj as acceptorWsgiObj
from leaderpaxos.share.urls import learn_paxos_leader
import time
import threading

def paxos_timer_acceptor(*args,**kwargs):
   
    start_time = args[0]
    val = acceptorWsgiObj.PAXOS_VALUE.get(learn_paxos_leader,acceptorWsgiObj.paxos_leader_default)
    current_time = val[1]
    
    if current_time > start_time:
        print 'acceptor leader updated, pass'
    else:
        print 'timeout, acceptor leader del'
        acceptorWsgiObj.PAXOS_VALUE.put(learn_paxos_leader,acceptorWsgiObj.paxos_leader_default)

