# -*- coding: utf-8 -*-

import time
import json
import threading

from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep,getQueuItem
from leaderpaxos.share.urls import learn_paxos_leader,identity_leader,identity_proposer,\
    broad_paxos_leader
from leaderpaxos.httpclient.libpaxos import paxos_alive
from leaderpaxos.thread.decision import identity_leader_process,identity_proposer_process,\
    item_communicate_broad_process,item_communicate_learn_process,item_decision_broad_process,\
    item_decision_learn_process

def paxos_state(host,port,hostUuid):
    
    while True:
        
        resp = paxos_alive(host, port)
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
            print hostUuid,wsgiObj.PAXOS_STATE.get(hostUuid,False)
        signal_sleep(wsgiObj,3)

def paxos_communicate(acceptorUuid,host,port):
    
    while True:
        
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        item = param.get('item')
        
        if learn_paxos_leader == item:
            item_communicate_learn_process(acceptorUuid,host,port)
            
        elif broad_paxos_leader == item:
            item_communicate_broad_process(acceptorUuid,host,port,param)
        else:
            pass
        
def paxos_decision():
    
    resp_learn_leader = []
    
    while True:
        
        acceptorUuid = getQueuItem(wsgiObj,wsgiObj.SIGNAL_RECV)
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        item = param.get('item')
        
        if learn_paxos_leader == item:
            val = param.get('val')
            item_decision_learn_process(acceptorUuid,resp_learn_leader,val)
        elif broad_paxos_leader == item:       
            item_decision_broad_process()
        else:
            pass
        
def paxos_proposer_main():
        
    wsgiObj.PAXOS_IDENTITY = identity_proposer
    import pdb;pdb.set_trace() 
    while True:
        if identity_proposer == wsgiObj.PAXOS_IDENTITY:
            identity_proposer_process()
                
        elif identity_leader == wsgiObj.PAXOS_IDENTITY:
            identity_leader_process()
    
