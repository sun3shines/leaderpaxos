# -*- coding: utf-8 -*-

import json
import threading
from leaderpaxos.share.urls import key_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.proposer.httpserver.static import wsgiObj

from leaderpaxos.httpclient.libpaxos import paxos_learn,paxos_broad
from leaderpaxos.share.http import http_success
from leaderpaxos.thread.communicate import paxos_broad_leader
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid


def item_base_learn_process(acceptorUuid,host,port,item):
    
    resp = paxos_learn(host, port, item)
    if http_success(resp):
        msgval = json.loads(resp.get('msg'))
        leaderUuid,leaderTerm,broadUuid = tuple(msgval)
        val = (leaderUuid,leaderTerm,broadUuid)
    else:
        val = ('failed',0,'')
    
    wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':item,'val':val})
    wsgiObj.SIGNAL_RECV.put(acceptorUuid)

def item_base_broad_process(acceptorUuid,host,port,param):
    
    item = param.get('item')
    val = param.get('val')
    broadUuid = param.get('broadUuid')
    paxos_broad(host, port, item, val, broadUuid)
    
def item_decision_learn_process(acceptorUuid,resp_learn_leader,val):
                
    leaderUuid,leaderTerm,broadUuid = val
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
        resp_learn_leader = []
        
def is_proposal():
    
    proposal = True
    for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        if True == wsgiObj.PAXOS_STATE.get(hostUuid,False):
            proposal = False    
            break
    if wsgiObj.leaderUuid and True == wsgiObj.PAXOS_STATE.get(wsgiObj.leaderUuid,False):
        proposal = False
        
    return proposal

def identity_proposer_process():
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':key_paxos_leader,
                                         'val':None})
        wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)
        
    leaderUuid,leaderTerm,broadUuid = wsgiObj.MAIN_LEARN_RECV.get()
    
    # 此处涉及到leader的重启了，如果是在任期内重启？和在任期外重启呢？ 
    if not leaderUuid:
        if is_proposal():
            print '%s to be new leader' % (wsgiObj.hostUuid)
            paxos_broad_leader(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
            signal_sleep(wsgiObj,wsgiObj.PAXOS_LEADER_TERM)
            
        else:
            signal_sleep(wsgiObj,wsgiObj.PAXOS_TRY_TERM)
    else:
        if wsgiObj.hostUuid == leaderUuid:
            # 任期内重启了            
            print '%s to be new leader' % (wsgiObj.hostUuid)
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
            signal_sleep(wsgiObj,leaderTerm)
        else:
            wsgiObj.leaderUuid = leaderUuid
            signal_sleep(wsgiObj,leaderTerm)

def identity_leader_process():
    
    print 'leader broad self info'
    paxos_broad_leader(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
    signal_sleep(wsgiObj,wsgiObj.LEADER_TIMER)
    
