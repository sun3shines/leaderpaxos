
import json
from leaderpaxos.share.http import jresponse
from leaderpaxos.accptor.httpserver.static import wsgiObj
def doTest(request):

    return jresponse('0','test ok',request,200)

def do_paxos_alive(request):

    return jresponse('0',wsgiObj.hostUuid,request,200)
    
def do_paxos_learn(request):
    
    param = json.loads(request.body)
    learn_item = param.get('learn_item')
    val = wsgiObj.PAXOS_VALUE.get(learn_item, '')
    return jresponse('0',val,request,200)