

from leaderpaxos.httpclient.libpaxos import paxos_alive
from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.share.urls import learn_paxos_leader
from leaderpaxos.httpclient.libpaxos import paxos_learn

def paxos_state(host,port,hostUuid):
    
    while True:
        
        resp = paxos_alive(host, port)
        if http_success(resp) and hostUuid.lower() == resp.get('msg','').lower():
            wsgiObj.PAXOS_STATE.put(hostUuid,True)
        else:
            wsgiObj.PAXOS_STATE.put(hostUuid,False)
        signal_sleep(2)
        
def display_state():
    
    while True:
        
        for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS:
            if hostUuid == wsgiObj.hostUuid:
                continue
            print hostUuid,wsgiObj.PAXOS_STATE.get(hostUuid,False)
        signal_sleep(3)

def paxos_communicate(hostUuid,host,port):
    
    while True:
        wsgiObj.SIGNAL_SEND.get(hostUuid).get()
        param = wsgiObj.CACHE_SEND.get(hostUuid)
        
        item = param.get('item')
        val = param.get('val')
        
        if learn_paxos_leader == item:
            resp = paxos_learn(host, port, item)
            if http_success(resp):
                pass
            else:
                wsgiObj.CACHE_RECV.put(hostUuid,{'item':learn_paxos_leader,
                                                 'val':'failed'})
            wsgiObj.SIGNAL_RECV.put(hostUuid)
            
        else:
            pass
        
def paxos_decision(hostUuid):
    
    resp_learn_leader = []
    resp_teach_leader = []
    
    while True:
        hostUuid = wsgiObj.SIGNAL_RECV.get()
        param = wsgiObj.CACHE_RECV.get(hostUuid)
        item = param.get('item')
        val = param.get('val')
        if learn_paxos_leader == item:
            resp_learn_leader.append(val)
            
        else:
            pass
        