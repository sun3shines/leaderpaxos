# -*- coding: utf-8 -*-

import json
from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 
from leaderpaxos.share.urls import strAlive,strLearn,strBroad
from leaderpaxos.share.urls import key_paxos_leader

class Alive(Task):
    def __init__(self,clientUuid):
        self.clientUuid = clientUuid
        
    def getUrl(self):
        return strAlive

    def getBody(self):
        return json.dumps({'clientUuid':self.clientUuid})
    
class Learn(Task):
    def __init__(self,item):
        self.item = item
        
    def getUrl(self):
        return strLearn
    
    def getBody(self):
        return json.dumps({'item':self.item})
    
class Broad(Task):
    def __init__(self,item,val,broadUuid):
        self.item = item
        self.val = val
        self.broadUuid = broadUuid
        
    def getUrl(self):
        return strBroad
    
    def getBody(self):
        return json.dumps({'item':self.item,
                           'val':self.val,'broadUuid':self.broadUuid})
        
def paxos_alive(host,port,clientUuid):
    
    t = Alive(clientUuid)
    mission.execute(t, host, port, 5)
    return t.response

def paxos_learn(host,port,item):
    
    t = Learn(item)
    mission.execute(t, host, port, 5)
    return t.response

def paxos_broad(host,port,item,val,broadUuid=''):
    t = Broad(item,val,broadUuid)
    mission.execute(t, host, port, 5)
    return t.response

def test():
    pass

if __name__ == '__main__':
    paxos_alive('127.0.0.1',10011,'')
    print paxos_learn('127.0.0.1',19011,'1')
#    print paxos_broad('127.0.0.1',19011,key_paxos_leader,'nSwfsePF-0GHDbc-KJcV')
    
