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

def item_proposer_learn(item):
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':item,
                                         'val':None})
        wsgiObj.SIGNAL_LEARN_SEND.get(hostUuid).put(0)
        
    val = wsgiObj.MAIN_LEARN_RECV.get()
    return val

def item_learn_transmit(acceptorUuid,host,port,item):
    
    resp = paxos_learn(host, port, item)
    if http_success(resp):
        msgval = json.loads(resp.get('msg'))
        leaderUuid,leaderTerm,broadUuid = tuple(msgval)
        val = (leaderUuid,leaderTerm,broadUuid)
    else:
        val = ('failed',0,'')
    
    wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':item,'val':val})
    wsgiObj.SIGNAL_LEARN_RECV.put(acceptorUuid)
    