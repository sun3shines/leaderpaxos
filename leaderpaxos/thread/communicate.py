# -*- coding: utf-8 -*-

from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid
from leaderpaxos.proposer.httpserver.static import wsgiObj

def paxos_broad_leader(item,val,broadUuid):
    
    broadUuid = get_broad_uuid()
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':item,'val':val,'broadUuid':broadUuid})
        wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)

