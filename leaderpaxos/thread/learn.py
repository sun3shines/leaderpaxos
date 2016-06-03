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
from leaderpaxos.share.signal import signal_sleep,getQueuItem

def item_proposer_learn(item):
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_LEARN_SEND.put(hostUuid,{'item':item,
                                         'val':None})
        wsgiObj.SIGNAL_LEARN_SEND.get(hostUuid).put(0)
        
    while True:
        qitem = getQueuItem(wsgiObj, wsgiObj.signalLearn)
        if qitem == item:
            break
        else:
            wsgiObj.signalLearn.put(qitem)
            signal_sleep(wsgiObj, 0.1)
    val = wsgiObj.cacheLearn.get(qitem)
    return val

def item_learn_transmit(acceptorUuid,host,port,item):
    
    resp = paxos_learn(host, port, item)
    if http_success(resp):
        if key_paxos_leader == item:
            msgval = json.loads(resp.get('msg'))
            val = tuple(msgval) # leaderUuid,leaderTerm,broadUuid = val
        else:
            val = resp.get('msg')
    else:
        val = 'failed'
    
    wsgiObj.CACHE_LEARN_RECV.put(acceptorUuid,{'item':item,'val':val})
    wsgiObj.SIGNAL_LEARN_RECV.put(acceptorUuid)
    
def paxos_learn_base(acceptorUuid,host,port):
    
    while True:
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_LEARN_SEND.get(acceptorUuid)
        item = param.get('item')
        item_learn_transmit(acceptorUuid,host,port,item)
        
def item_decision(acceptorUuid,param):
    
    item = param.get('item')
    val = param.get('val')
    print 'learn %s %s from acceptor %s ' % (item,val,acceptorUuid)
    
    if item not in wsgiObj.itemdict:
        wsgiObj.itemdict[item] = []
        
    itemval = val
    wsgiObj.itemdict[item].append(itemval)
    
    if len(wsgiObj.itemdict[item]) == len(wsgiObj.PAXOS_ACCEPTORS):
        if item == key_paxos_leader:
            learn_data = wsgiObj.paxos_leader_default
        else:
            learn_data = ''
            
        for val in wsgiObj.itemdict[item]:
            if val == 'failed':
                continue
            
            if item == key_paxos_leader:
                leaderUuid,leaderTerm,broadUuid = val
                if not leaderUuid:
                    continue
            else:
                if not val:
                    continue
                
            learn_data = val
            break
        
        wsgiObj.cacheLearn.put(item,learn_data)
        wsgiObj.signalLearn.put(item)
        wsgiObj.itemdict[item] = []
                                 
def paxos_decision():
    
    while True:
        acceptorUuid = getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_RECV)
        param = wsgiObj.CACHE_LEARN_RECV.get(acceptorUuid)
        item_decision(acceptorUuid,param)
        