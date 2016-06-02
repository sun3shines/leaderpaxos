# -*- coding: utf-8 -*-

from leaderpaxos.thread.identity import proposer,leader,init_identity,is_leader,is_proposer

# 因为是相同的队列，所以导致了paxos_learn_base 和 paxos_broad_base 发生了抢占
# 因此会出现每次调试运行的结果不同了。
                                
def paxos_proposer_main():

    init_identity()
    while True:
        print 'loop'
        if is_proposer():
            proposer()
        elif is_leader():
            leader()
    
