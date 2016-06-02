# -*- coding: utf-8 -*-

from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import getQueuItem
from leaderpaxos.thread.decision import item_decision
from leaderpaxos.thread.identity import proposer,leader,init_identity,is_leader,is_proposer

# 因为是相同的队列，所以导致了paxos_learn_base 和 paxos_broad_base 发生了抢占
# 因此会出现每次调试运行的结果不同了。
                        
def paxos_decision():
    
    resp_learn_leader = []
    while True:
        acceptorUuid = getQueuItem(wsgiObj,wsgiObj.SIGNAL_LEARN_RECV)
        param = wsgiObj.CACHE_RECV.get(acceptorUuid)
        item = param.get('item')
        val = param.get('val')
        print 'learn %s %s from acceptor %s ' % (item,val,acceptorUuid)
        item_decision(acceptorUuid, resp_learn_leader, item, val)
        
def paxos_proposer_main():

    init_identity()
    
    while True:
        print 'loop'
        if is_proposer():
            proposer()
        elif is_leader():
            leader()
    
