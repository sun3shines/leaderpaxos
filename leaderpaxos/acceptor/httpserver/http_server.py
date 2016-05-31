# -*- coding: utf-8 -*-

import json
import time
import threading
from leaderpaxos.share.http import jresponse
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import learn_paxos_leader,broad_paxos_leader
from leaderpaxos.thread.libtimer import paxos_timer_acceptor
from leaderpaxos.thread.communicate import acceptor_broadcast

def doTest(request):

    return jresponse('0','test ok',request,200)
    
def do_paxos_learn(request):

    param = json.loads(request.body)
    item = param.get('item')
    if item == learn_paxos_leader:
        leaderUuid,leaderTime,broadUuid = wsgiObj.PAXOS_VALUE.get(learn_paxos_leader, wsgiObj.paxos_leader_default)
        if not leaderUuid:
            msgval = json.dumps(wsgiObj.paxos_leader_default)
        else:
            leaderTerm = wsgiObj.PAXOS_LEADER_TERM - (time.time()-leaderTime)
            msgval = json.dumps((leaderUuid,leaderTerm,broadUuid))
    else:
        msgval = ''
        
    return jresponse('0',msgval,request,200)

def do_paxos_broad(request):
    
    param = json.loads(request.body)
    item = param.get('item')
    
    if item == broad_paxos_leader:
        leaderUuid = param.get('val')
        leaderTime = time.time()
        broadUuid = param.get('broadUuid')
        if broadUuid == wsgiObj.broadUuid:
            pass
        else:
            key = learn_paxos_leader
            val = (leaderUuid,leaderTime,broadUuid)
            wsgiObj.PAXOS_QUEUE.put((key,val))
            acceptor_broadcast(broad_paxos_leader, leaderUuid, broadUuid)
    
    return jresponse('0','',request,200)

