# -*- coding: utf-8 -*-

from leaderpaxos.share.urls import key_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.proposer.httpserver.static import wsgiObj

from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid
from leaderpaxos.share.string import str_equal

from leaderpaxos.thread.priority import is_proposal
from leaderpaxos.thread.learn import item_proposer_learn
from leaderpaxos.thread.broad import item_proposer_broad

def promote(sleep_time = wsgiObj.PAXOS_LEADER_TERM):
    wsgiObj.leaderUuid = wsgiObj.hostUuid
    wsgiObj.PAXOS_IDENTITY = identity_leader
    signal_sleep(sleep_time)
            
def init_identity():
    wsgiObj.PAXOS_IDENTITY = identity_proposer

def is_proposer():
    return identity_proposer == wsgiObj.PAXOS_IDENTITY

def is_leader():
    return identity_leader == wsgiObj.PAXOS_IDENTITY
    
def proposer():
    
    leaderUuid,leaderTerm,broadUuid = item_proposer_learn(key_paxos_leader)
    print 'learn leader %s from acceptor' % (leaderUuid)
    leaderTerm = int(leaderTerm)
    if not leaderUuid:
        if is_proposal():
            print 'going to be new leader' ,wsgiObj.hostUuid
            item_proposer_broad(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
            promote()
        else:
            print 'because proposal ,try again'
            signal_sleep(wsgiObj,wsgiObj.PAXOS_TRY_TERM)
    else:
        if str_equal(wsgiObj.hostUuid, leaderUuid):
            print 'alread to be new leader' ,wsgiObj.hostUuid
            promote(leaderTerm)
        else:
            print 'learn leader as %s' % (leaderUuid)
            wsgiObj.leaderUuid = leaderUuid
            signal_sleep(wsgiObj,leaderTerm)

def leader():
    print 'leader broad self info'
    item_proposer_broad(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
    signal_sleep(wsgiObj,wsgiObj.PAXOS_LEADER_TERM)
    