# -*- coding: utf-8 -*-

from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.urls import broad_paxos_leader

def paxos_broad_leader():
    broadUuid = get_broad_uuid()
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        val = (wsgiObj.hostUuid,broadUuid)
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':broad_paxos_leader,'val':val})
        wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)
