# -*- coding: utf-8 -*-

import json
import time
from leaderpaxos.share.http import jresponse
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import key_paxos_leader
from leaderpaxos.thread.acceptor import acceptor_broadcast
from leaderpaxos.share.string import str_equal

def doTest(request):

    return jresponse('0','test ok',request,200)
    
def do_paxos_learn(request):

    param = json.loads(request.body)
    item = param.get('item')
    if str_equal(item ,key_paxos_leader):
        leaderUuid,leaderTime,broadUuid = wsgiObj.PAXOS_VALUE.get(key_paxos_leader, wsgiObj.paxos_leader_default)
        if not leaderUuid:
            msgval = json.dumps(wsgiObj.paxos_leader_default)
        else:
            leaderTerm = wsgiObj.PAXOS_LEADER_TERM - (time.time()-leaderTime)
            msgval = json.dumps((leaderUuid,leaderTerm,broadUuid))
    else:
        msgval = wsgiObj.PAXOS_VALUE.get(item,'')
    return jresponse('0',msgval,request,200)

def do_paxos_broad(request):

    param = json.loads(request.body)
    item = param.get('item')

    broadUuid = param.get('broadUuid')
    if not broadUuid:
        return jresponse('-1','broadUuid error',request,200)

    if str_equal(item ,key_paxos_leader):
        
        leaderUuid = param.get('val')
        leaderTime = time.time()
        if broadUuid == wsgiObj.broadUuid:
            pass
        else:
            val = (leaderUuid,leaderTime,broadUuid)
            wsgiObj.PAXOS_QUEUE.put((item,val))
            acceptor_broadcast(item, leaderUuid, broadUuid)
    else:
        val = param.get('val')
        if broadUuid == wsgiObj.itemBroadUuid.get(item,''):
            pass
        else:
            wsgiObj.itemBroadUuid.put(item,broadUuid)
            wsgiObj.PAXOS_VALUE.put(item,val)
            acceptor_broadcast(item, val, broadUuid)
            
    return jresponse('0','',request,200)

