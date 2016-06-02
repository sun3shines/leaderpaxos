# -*- coding: utf-8 -*-

from leaderpaxos.share.urls import key_paxos_leader
from leaderpaxos.proposer.httpserver.static import wsgiObj

def item_decision(acceptorUuid,res,item,val):
    
    if item == key_paxos_leader:
        leaderUuid,leaderTerm,broadUuid = val
        res.append((acceptorUuid,leaderUuid,leaderTerm,broadUuid))
        if len(res) == len(wsgiObj.PAXOS_ACCEPTORS):
            learn_leader_data = wsgiObj.paxos_leader_default
            for acceptorUuid,leaderUuid,leaderTerm,broadUuid in res:
                if not leaderUuid or 'failed' == leaderUuid:
                    continue
                learn_leader_data = (leaderUuid,leaderTerm,broadUuid)
                break
            
            wsgiObj.MAIN_LEARN_RECV.put(learn_leader_data)
            res = []
    return res
