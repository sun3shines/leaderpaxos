# -*- coding: utf-8 -*-

import threading
from leaderpaxos.acceptor.httpserver.static import wsgiObj
from leaderpaxos.share.urls import identiry_acceptor,key_paxos_leader
from leaderpaxos.httpclient.libpaxos import paxos_broad
from leaderpaxos.thread.libtimer import paxos_timer_acceptor
from leaderpaxos.share.signal import getQueuItem
from leaderpaxos.share.string import str_equal

def acceptor_broadcast(item,val,broadUuid):
    
    for hostUuid,_,_ in wsgiObj.PAXOS_ACCEPTORS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        wsgiObj.CACHE_SEND.put(hostUuid,{'item':item,'val':val,'broadUuid':broadUuid})
        wsgiObj.SIGNAL_BROAD_SEND.get(hostUuid).put(0)
        
def paxos_acceptor_main():
    
    wsgiObj.PAXOS_IDENTITY = identiry_acceptor
    
    while True:
        
        key,val = getQueuItem(wsgiObj,wsgiObj.PAXOS_QUEUE)
        if str_equal(key ,key_paxos_leader):
            leaderUuid,leaderTime,broadUuid = val
            wsgiObj.broadUuid = broadUuid
            # print 'get info %s %s' % (key_paxos_leader,leaderUuid)
            start_time = leaderTime
            wsgiObj.PAXOS_VALUE.put(key_paxos_leader,val)
            threading.Timer(wsgiObj.PAXOS_LEADER_TERM,paxos_timer_acceptor,[start_time]).start()
        else:
            # print 'get info %s' % (key)
            pass
            
def paxos_acceptor_broadcast(acceptorUuid,host,port):
    
    while True:
        
        getQueuItem(wsgiObj,wsgiObj.SIGNAL_BROAD_SEND.get(acceptorUuid))
        param = wsgiObj.CACHE_SEND.get(acceptorUuid)
        broadUuid = param.get('broadUuid')
        item = param.get('item')
        val = param.get('val')
        paxos_broad(host, port, item, val, broadUuid)

class do_paxos_acceptor(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            paxos_acceptor_main()
        except:
            pass   
    
class do_acceptor_broad(threading.Thread):
    
    def __init__(self,acceptorUuid,host,port):
        
        threading.Thread.__init__(self)
        self.acceptorUuid = acceptorUuid
        self.host = host
        self.port = port
        
    def run(self):
        try:
            paxos_acceptor_broadcast(self.acceptorUuid, self.host, self.port)
        except:
            pass
    