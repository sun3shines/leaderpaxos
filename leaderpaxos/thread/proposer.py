# -*- coding: utf-8 -*-

import time
import json
import threading
from leaderpaxos.httpclient.libpaxos import paxos_alive
from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.share.urls import learn_paxos_leader,identity_leader,identity_proposer,\
    broad_paxos_leader
from leaderpaxos.httpclient.libpaxos import paxos_learn,paxos_broad
from leaderpaxos.thread.decision import is_proposal
from leaderpaxos.thread.libtimer import paxos_timer_leader
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid

def paxos_state(host,port,hostUuid):
    
    while True:
        
        resp = paxos_alive(host, port)
        if http_success(resp) and hostUuid.lower() == resp.get('msg','').lower():
            wsgiObj.PAXOS_STATE.put(hostUuid,True)
        else:
            wsgiObj.PAXOS_STATE.put(hostUuid,False)
        signal_sleep(2)
        
def display_state():
    
    while True:
        
        for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS:
            if hostUuid == wsgiObj.hostUuid:
                continue
            print hostUuid,wsgiObj.PAXOS_STATE.get(hostUuid,False)
        signal_sleep(3)

def paxos_communicate(acceptorUuid,host,port):
    
    while True:
        wsgiObj.SIGNAL_SEND.get(acceptorUuid).get()
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        
        item = param.get('item')
        
        if learn_paxos_leader == item:
            resp = paxos_learn(host, port, learn_paxos_leader)
            
            if http_success(resp):
                msgval = json.loads(resp.get('msg'))
                leaderUuid,leaderTerm,broadUuid = tuple(msgval)
                wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':learn_paxos_leader,
                                                 'val':(leaderUuid,leaderTerm,broadUuid)})
            else:
                wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':learn_paxos_leader,
                                                 'val':('failed',0,'')})
            wsgiObj.SIGNAL_RECV.put(acceptorUuid)
            
        elif broad_paxos_leader == item:
            leaderUuid,broaduuid = param.get('val')
            paxos_broad(host, port, broad_paxos_leader, leaderUuid, broaduuid)
            
        else:
            pass
        
def paxos_decision():
    
    resp_learn_leader = []
    resp_broad_leader = []
    
    while True:
        acceptorUuid = wsgiObj.SIGNAL_RECV.get()
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        item = param.get('item')
        val = param.get('val')
        leaderUuid,leaderTerm,broadUuid = val
        
        if learn_paxos_leader == item:
            resp_learn_leader.append((acceptorUuid,leaderUuid,leaderTerm,broadUuid))
            if len(resp_learn_leader) == len(wsgiObj.PAXOS_ACCEPTORS):
                learn_leader_data = wsgiObj.paxos_leader_default
                for acceptorUuid,leaderUuid,leaderTerm,broadUuid in resp_learn_leader:
                    if not leaderUuid or 'failed' == leaderUuid:
                        continue
                    print 'learn leader %s %s from acceptor %s ' % (leaderUuid,leaderTerm,acceptorUuid)
                    learn_leader_data = (leaderUuid,leaderTerm,broadUuid)
                    break
                
                wsgiObj.MAIN_LEARN_RECV.put(learn_leader_data)
        else:       
            pass
        
def paxos_proposer_main():
        
    wsgiObj.PAXOS_IDENTITY = identity_proposer
    
    while True:
        
        for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
            wsgiObj.CACHE_SEND.put(hostUuid,{'item':learn_paxos_leader,
                                             'val':None})
            wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)
            
        leaderUuid,leaderTerm,broadUuid = wsgiObj.MAIN_LEARN_RECV.get()
        # 此处涉及到leader的重启了，如果是在任期内重启？和在任期外重启呢？ 
        if not leaderUuid:
            if is_proposal():
                timer = wsgiObj.LEADER_TIMER
                wsgiObj.LEADER_TIMER = threading.Timer(wsgiObj.PAXOS_LEADER_TERM,paxos_timer_leader)

                broadUuid = get_broad_uuid()
                for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
                    wsgiObj.CACHE_SEND.put(hostUuid,{'item':broad_paxos_leader,
                                                     'val':(wsgiObj.hostUuid,broadUuid)})
                    wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)
                    
                wsgiObj.leaderUuid = wsgiObj.hostUuid
                wsgiObj.broadUuid = broadUuid
                
                if timer:
                    timer.cancel()
                signal_sleep(wsgiObj.PAXOS_LEADER_TERM)
                
            else:
                signal_sleep(wsgiObj.PAXOS_TRY_TERM)
        else:
            print 'the leader is %s, sleep time %s' % (leaderUuid,leaderTerm)
            wsgiObj.leaderUuid = leaderUuid
            wsgiObj.broadUuid = broadUuid
            signal_sleep(leaderTerm)
            
    
