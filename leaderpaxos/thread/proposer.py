# -*- coding: utf-8 -*-

import time
import json
import threading

from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep,getQueuItem
from leaderpaxos.share.urls import key_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.httpclient.libpaxos import paxos_alive,paxos_broad
from leaderpaxos.thread.decision import identity_leader_process,identity_proposer_process,\
    item_base_broad_process,item_base_learn_process,key_paxos_leader_decision
from leaderpaxos.share.string import str_equal

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
        item_base_learn_process(acceptorUuid,host,port,item)
            
def paxos_broad_base(acceptorUuid,host,port):
    
    while True:
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_BROAD_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        item_base_broad_process(acceptorUuid, host, port, param)
            
def paxos_decision():
    
    resp_learn_leader = []
    
    while True:
        
        acceptorUuid = getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_RECV)
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        # print acceptorUuid,param
        item = param.get('item')
        
        if key_paxos_leader == item:
            val = param.get('val')
            resp_learn_leader = key_paxos_leader_decision(acceptorUuid,resp_learn_leader,val)
        else:
            pass
        
def paxos_proposer_main():

    wsgiObj.PAXOS_IDENTITY = identity_proposer
    while True:
        print 'loop again'
        if identity_proposer == wsgiObj.PAXOS_IDENTITY:
            identity_proposer_process()
                
        elif identity_leader == wsgiObj.PAXOS_IDENTITY:
            identity_leader_process()
    
