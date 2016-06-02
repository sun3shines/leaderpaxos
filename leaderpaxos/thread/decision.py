# -*- coding: utf-8 -*-

from leaderpaxos.share.urls import key_paxos_leader
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import getQueuItem

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
    
def paxos_decision():
    
    while True:
        acceptorUuid = getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_RECV)
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        item = param.get('item')
        val = param.get('val')
        print 'learn %s %s from acceptor %s ' % (item,val,acceptorUuid)
        if item not in wsgiObj.itemdict:
            wsgiObj.itemdict[item] = []
        item_decision(acceptorUuid,item, val)
        