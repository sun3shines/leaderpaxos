# -*- coding: utf-8 -*-

import json
import threading
from leaderpaxos.share.urls import key_paxos_leader,identity_leader,identity_proposer
from leaderpaxos.share.signal import signal_sleep
from leaderpaxos.proposer.httpserver.static import wsgiObj

from leaderpaxos.httpclient.libpaxos import paxos_learn,paxos_broad
from leaderpaxos.share.http import http_success
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuid
from leaderpaxos.share.string import str_equal

from leaderpaxos.thread.decision import is_proposal
from leaderpaxos.thread.learn import item_proposer_learn
from leaderpaxos.thread.broad import item_proposer_broad

def identity_proposer_process():
    
    leaderUuid,leaderTerm,broadUuid = item_proposer_learn(key_paxos_leader)
    print 'learn leader %s from acceptor' % (leaderUuid)
    leaderTerm = int(leaderTerm)
    if not leaderUuid:
        if is_proposal():
            print 'going to be new leader' ,wsgiObj.hostUuid
            item_proposer_broad(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
            signal_sleep(wsgiObj,wsgiObj.PAXOS_LEADER_TERM)
            
        else:
            print 'because proposal ,try again'
            signal_sleep(wsgiObj,wsgiObj.PAXOS_TRY_TERM)
    else:
        if str_equal(wsgiObj.hostUuid, leaderUuid):
            # 任期内重启了            
            print 'alread to be new leader' ,wsgiObj.hostUuid
            wsgiObj.leaderUuid = wsgiObj.hostUuid
            wsgiObj.PAXOS_IDENTITY = identity_leader
            signal_sleep(wsgiObj,leaderTerm)
        else:
            print 'learn leader as %s' % (leaderUuid)
            wsgiObj.leaderUuid = leaderUuid
            signal_sleep(wsgiObj,leaderTerm)

def identity_leader_process():
    
    print 'leader broad self info'
    item_proposer_broad(key_paxos_leader,wsgiObj.hostUuid,get_broad_uuid())
    signal_sleep(wsgiObj,wsgiObj.PAXOS_LEADER_TERM)
    