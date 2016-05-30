
import json
import time
from leaderpaxos.share.http import jresponse
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import learn_paxos_leader,teach_paxos_leader

def doTest(request):

    return jresponse('0','test ok',request,200)
    
def do_paxos_learn(request):

    param = json.loads(request.body)
    learn_item = param.get('learn_item')
    if learn_item == learn_paxos_leader:
        leaderUuid,leaderTime = wsgiObj.PAXOS_VALUE.get(learn_paxos_leader, ('',0))
        if not leaderUuid:
            msgval = json.dumps(('',0))
        else:
            leaderTerm = wsgiObj.PAXOS_LEADER_TERM - (time.time()-leaderTime)
            msgval = json.dumps((leaderUuid,leaderTerm))
    else:
        msgval = ''
        
    return jresponse('0',msgval,request,200)
