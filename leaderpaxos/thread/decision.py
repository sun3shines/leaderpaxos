# -*- coding: utf-8 -*-

import json
import threading
from leaderpaxos.share.urls import key_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.proposer.httpserver.static import wsgiObj

from leaderpaxos.httpclient.libpaxos import paxos_learn,paxos_broad
from leaderpaxos.share.http import http_success
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid
from leaderpaxos.share.string import str_equal

def leader_broadcast(item,val,broadUuid):
    
    broadUuid = get_broad_uuid()
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':item,'val':val,'broadUuid':broadUuid})
        wsgiObj.SIGNAL_BROAD_SEND.get(hostUuid).put(0)

def item_proposer_learn(item):
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':item,
                                         'val':None})
        wsgiObj.SIGNAL_LEARN_SEND.get(hostUuid).put(0)
        
    val = wsgiObj.MAIN_LEARN_RECV.get()
    return val

def item_base_learn_process(acceptorUuid,host,port,item):
    
    resp = paxos_learn(host, port, item)
    if http_success(resp):
        msgval = json.loads(resp.get('msg'))
        leaderUuid,leaderTerm,broadUuid = tuple(msgval)
        val = (leaderUuid,leaderTerm,broadUuid)
    else:
        val = ('failed',0,'')
    
    wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':item,'val':val})
    wsgiObj.SIGNAL_LEARN_RECV.put(acceptorUuid)

def item_base_broad_process(acceptorUuid,host,port,param):
    
    item = param.get('item')
    val = param.get('val')
    broadUuid = param.get('broadUuid')
    paxos_broad(host, port, item, val, broadUuid)
    
def key_paxos_leader_decision(acceptorUuid,resp_learn_leader,val):
                
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
    
    leaderUuid,leaderTerm,broadUuid = item_proposer_learn(key_paxos_leader)
    leaderTerm = int(leaderTerm)
    if not leaderUuid:
        if is_proposal():
            print 'going to be new leader' ,wsgiObj.hostUuid
            leader_broadcast(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
            signal_sleep(wsgiObj,wsgiObj.PAXOS_LEADER_TERM)
            
        else:
            print 'because proposal ,try again'
            signal_sleep(wsgiObj,wsgiObj.PAXOS_TRY_TERM)
    else:
        if str_equal(wsgiObj.hostUuid, leaderUuid):
            # 任期内重启了            
            print 'alread to be new leader' ,wsgiObj.hostUuid
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
            signal_sleep(wsgiObj,leaderTerm)
        else:
            print 'learn leader as %s' % (leaderUuid)
            wsgiObj.leaderUuid = leaderUuid
            signal_sleep(wsgiObj,leaderTerm)

def identity_leader_process():
    
    print 'leader broad self info'
    leader_broadcast(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
    signal_sleep(wsgiObj,wsgiObj.PAXOS_LEADER_TERM)
    
