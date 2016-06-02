# -*- coding: utf-8 -*-

import time
import json
import threading

from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep,getQueuItem
from leaderpaxos.share.urls import key_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.httpclient.libpaxos import paxos_alive
from leaderpaxos.thread.decision import item_decision
from leaderpaxos.thread.learn import item_proposer_learn,item_learn_transmit
from leaderpaxos.thread.broad import item_proposer_broad,item_broad_transmit
from leaderpaxos.thread.identity import identity_leader_process,identity_proposer_process

def paxos_state(host,port,hostUuid):
    
    while True:
        
        resp = paxos_alive(host, port,wsgiObj.hostUuid)
        if http_success(resp) and hostUuid.lower() == resp.get('msg','').lower():
            wsgiObj.PAXOS_STATE.put(hostUuid,True)
        else:
            wsgiObj.PAXOS_STATE.put(hostUuid,False)
        signal_sleep(wsgiObj,2)
        
def display_state():
    
    while True:
        
        for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS:
            if hostUuid == wsgiObj.hostUuid:
                continue
            # print hostUuid,wsgiObj.PAXOS_STATE.get(hostUuid,False)
        signal_sleep(wsgiObj,3)

# 因为是相同的队列，所以导致了paxos_learn_base 和 paxos_broad_base 发生了抢占
# 因此会出现每次调试运行的结果不同了。

def paxos_learn_base(acceptorUuid,host,port):
    
    while True:
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        item = param.get('item')
        item_learn_transmit(acceptorUuid,host,port,item)
            
def paxos_broad_base(acceptorUuid,host,port):
    
    while True:
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_BROAD_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        item_broad_transmit(acceptorUuid, host, port, param)
            
def paxos_decision():
    
    resp_learn_leader = []
    
    while True:
        acceptorUuid = getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_RECV)
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        item = param.get('item')
        val = param.get('val')
        item_decision(acceptorUuid, resp_learn_leader, item, val)
        
def paxos_proposer_main():

    wsgiObj.PAXOS_IDENTITY = identity_proposer
    while True:
        print 'loop again'
        if identity_proposer == wsgiObj.PAXOS_IDENTITY:
            identity_proposer_process()
                
        elif identity_leader == wsgiObj.PAXOS_IDENTITY:
            identity_leader_process()
    
