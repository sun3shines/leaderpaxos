# -*- coding: utf-8 -*-

from leaderpaxos.share.urls import key_paxos_leader
from leaderpaxos.proposer.httpserver.static import wsgiObj

def item_decision(acceptorUuid,item,val):
    
    if item == key_paxos_leader:
        leaderUuid,leaderTerm,broadUuid = val
        wsgiObj.itemdict[item].append((acceptorUuid,leaderUuid,leaderTerm,broadUuid))
        if len(wsgiObj.itemdict[item]) == len(wsgiObj.PAXOS_ACCEPTORS):
            learn_leader_data = wsgiObj.paxos_leader_default
            for acceptorUuid,leaderUuid,leaderTerm,broadUuid in wsgiObj.itemdict[item]:
                if not leaderUuid or 'failed' == leaderUuid:
                    continue
                learn_leader_data = (leaderUuid,leaderTerm,broadUuid)
                break
            wsgiObj.cacheLearn.put(item,learn_leader_data)
            wsgiObj.signalLearn.put(item)
            wsgiObj.itemdict[item] = []
    