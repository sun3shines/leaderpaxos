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


def item_decision(acceptorUuid,res,item,val):
    
    if item == key_paxos_leader:
        leaderUuid,leaderTerm,broadUuid = val
        res.append((acceptorUuid,leaderUuid,leaderTerm,broadUuid))
        if len(res) == len(wsgiObj.PAXOS_ACCEPTORS):
            learn_leader_data = wsgiObj.paxos_leader_default
            for acceptorUuid,leaderUuid,leaderTerm,broadUuid in res:
                if not leaderUuid or 'failed' == leaderUuid:
                    continue
                print 'learn leader %s %s from acceptor %s ' % (leaderUuid,leaderTerm,acceptorUuid)
                learn_leader_data = (leaderUuid,leaderTerm,broadUuid)
                break
            
            wsgiObj.MAIN_LEARN_RECV.put(learn_leader_data)
            res = []
    return res

def is_proposal():
    
    proposal = True
    for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS[:wsgiObj.procindex]:
        if hostUuid == wsgiObj.hostUuid:
            continue
        if True == wsgiObj.PAXOS_STATE.get(hostUuid,False):
            proposal = False    
            break
    if wsgiObj.leaderUuid and wsgiObj.PAXOS_STATE.get(wsgiObj.leaderUuid,False):
        print 'leader state True'
        proposal = False
    else:
        # print wsgiObj.leaderUuid,wsgiObj.PAXOS_STATE.get(wsgiObj.leaderUuid,False)
        print 'leader state False'
        
    return proposal

