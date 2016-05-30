# -*- coding: utf-8 -*-

import json
import threading
from leaderpaxos.share.urls import learn_paxos_leader,broad_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.thread.libtimer import paxos_timer_leader
from leaderpaxos.httpclient.libpaxos import paxos_learn,paxos_broad
from leaderpaxos.share.http import http_success
from leaderpaxos.thread.communicate import paxos_broad_leader

def item_communicate_learn_process(acceptorUuid,host,port):
    
    resp = paxos_learn(host, port, learn_paxos_leader)
    if http_success(resp):
        msgval = json.loads(resp.get('msg'))
        leaderUuid,leaderTerm,broadUuid = tuple(msgval)
        val = (leaderUuid,leaderTerm,broadUuid)
    else:
        val = ('failed',0,'')
    
    wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':learn_paxos_leader,'val':val})
    wsgiObj.SIGNAL_RECV.put(acceptorUuid)

def item_communicate_broad_process(acceptorUuid,host,port,val):
    leaderUuid,broaduuid = val
    paxos_broad(host, port, broad_paxos_leader, leaderUuid, broaduuid)

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
        
def item_decision_broad_process():
    pass

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
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':learn_paxos_leader,
                                         'val':None})
        wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)
        
    leaderUuid,leaderTerm,broadUuid = wsgiObj.MAIN_LEARN_RECV.get()
    # 此处涉及到leader的重启了，如果是在任期内重启？和在任期外重启呢？ 
    if not leaderUuid:
        if is_proposal():
            timer = wsgiObj.LEADER_TIMER
            wsgiObj.LEADER_TIMER = threading.Timer(wsgiObj.PAXOS_LEADER_TERM,paxos_timer_leader)
            wsgiObj.LEADER_TIMER.start()
            paxos_broad_leader()
                
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.broadUuid = broadUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
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

def identity_leader_process():
    pass
