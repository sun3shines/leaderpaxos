# -*- coding: utf-8 -*-

from leaderpaxos.proposer.httpserver.static import wsgiObj

def is_proposal():
    
    proposal = True
    for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS:
        if hostUuid == wsgiObj.hostUuid:
            continue
        if True == wsgiObj.PAXOS_STATE.get(hostUuid,False):
            proposal = False    
            break
    if wsgiObj.leaderUuid and True == wsgiObj.PAXOS_STATE.get(wsgiObj.leaderUuid,False):
        proposal = False
        
    return proposal

