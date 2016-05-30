# -*- coding: utf-8 -*-

import json
import time
import threading
from leaderpaxos.share.http import jresponse
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import learn_paxos_leader,teach_paxos_leader,\
    broad_paxos_leader
from leaderpaxos.thread.libtimer import paxos_timer_acceptor

def doTest(request):

    return jresponse('0','test ok',request,200)
    
def do_paxos_learn(request):

    param = json.loads(request.body)
    learn_item = param.get('learn_item')
    if learn_item == learn_paxos_leader:
        leaderUuid,leaderTime,broadUuid = wsgiObj.PAXOS_VALUE.get(learn_paxos_leader, ('',0,''))
        if not leaderUuid:
            msgval = json.dumps(('',0,0))
        else:
            leaderTerm = wsgiObj.PAXOS_LEADER_TERM - (time.time()-leaderTime)
            msgval = json.dumps((leaderUuid,leaderTerm,broadUuid))
    else:
        msgval = ''
        
    return jresponse('0',msgval,request,200)

def do_paxos_broad(request):
    
    param = json.loads(request.body)
    broad_item = param.get('broad_item')
    
    if broad_item == broad_paxos_leader:
        leaderUuid = param.get('val')
        leaderTime = time.time()
        broadUuid = param.get('broad_uuid')
        if broadUuid == wsgiObj.broadUuid:
            pass
        else:
            wsgiObj.PAXOS_VALUE.put(learn_paxos_leader,(leaderUuid,leaderTime,broadUuid))
            
            timer = wsgiObj.PAXOS_TIMER
            wsgiObj.PAXOS_TIMER = threading.Timer(wsgiObj.PAXOS_LEADER_TERM,paxos_timer_acceptor)
            if timer:
                timer.cancel()
    
    return jresponse('0','',request,200)

