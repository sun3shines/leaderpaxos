# -*- coding: utf-8 -*-

import json
import threading
from leaderpaxos.proposer.httpserver.static import wsgiObj

from leaderpaxos.httpclient.libpaxos import paxos_broad
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid
from leaderpaxos.share.signal import getQueuItem

def item_proposer_broad(item,val,broadUuid):
    
    broadUuid = get_broad_uuid()
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':item,'val':val,'broadUuid':broadUuid})
        wsgiObj.SIGNAL_BROAD_SEND.get(hostUuid).put(0)
        
def item_broad_transmit(acceptorUuid,host,port,param):
    
    item = param.get('item')
    val = param.get('val')
    broadUuid = param.get('broadUuid')
    paxos_broad(host, port, item, val, broadUuid)
    
def paxos_broad_base(acceptorUuid,host,port):
    
    while True:
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_BROAD_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        item_broad_transmit(acceptorUuid, host, port, param)
        