
import time
import json
from leaderpaxos.httpclient.libpaxos import paxos_alive
from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.share.urls import learn_paxos_leader,identity_leader,identity_proposer
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

def paxos_communicate(acceptorUuid,host,port):
    
    while True:
        wsgiObj.SIGNAL_SEND.get(acceptorUuid).get()
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        
        item = param.get('item')
        val = param.get('val')
        
        if learn_paxos_leader == item:
            resp = paxos_learn(host, port, learn_paxos_leader)
            if http_success(resp):
                msgval = json.loads(resp.get('msg'))
                leaderUuid,leaderTerm = tuple(msgval)
                wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':learn_paxos_leader,
                                                 'val':(leaderUuid,leaderTerm)})
            else:
                wsgiObj.CACHE_RECV.put(acceptorUuid,{'item':learn_paxos_leader,
                                                 'val':('failed',0)})
            wsgiObj.SIGNAL_RECV.put(acceptorUuid)
            
        else:
            pass
        
def paxos_decision():
    
    resp_learn_leader = []
    resp_teach_leader = []
    
    while True:
        acceptorUuid = wsgiObj.SIGNAL_RECV.get()
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        item = param.get('item')
        val = param.get('val')
        leaderUuid,leaderTerm = val
        
        if learn_paxos_leader == item:
            resp_learn_leader.append((acceptorUuid,leaderUuid,leaderTerm))
            learn_leader_data = ('',0)
            if len(resp_learn_leader) == len(wsgiObj.PAXOS_ACCEPTORS):
                for acceptorUuid,leaderUuid,leaderTerm in resp_learn_leader:
                    if not leaderUuid or 'failed' == leaderUuid:
                        continue
                    print 'learn leader %s %s from acceptor %s ' % (leaderUuid,leaderTerm,acceptorUuid)
                    learn_leader_data = (leaderUuid,leaderTerm)
                wsgiObj.MAIN_LEARN_RECV.put(learn_leader_data)
        else:       
            pass
        
def paxos_proposer_main():
    
    wsgiObj.PAXOS_IDENTITY = identity_proposer
    
    while True:
        for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
            wsgiObj.CACHE_SEND.put(hostUuid,{'item':learn_paxos_leader,
                                             'val':None})
            wsgiObj.SIGNAL_SEND.get(hostUuid).put(0)
            
        leaderUuid,leaderTerm = wsgiObj.MAIN_LEARN_RECV.get()
            
        if not leaderUuid:
            print 'data is none,prepare to proposal'
            import pdb;pdb.set_trace()
        else:
            print 'the leader is %s, sleep time %s' % (leaderUuid,leaderTerm)
            signal_sleep(leaderTerm)
        
    