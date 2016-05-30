# -*- coding: utf-8 -*-

import json
from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 
from leaderpaxos.share.urls import strAlive,strLearn,strTeach
from leaderpaxos.share.urls import learn_paxos_leader,teach_paxos_leader

class Alive(Task):
    def getUrl(self):
        return strAlive

class Learn(Task):
    def __init__(self,learn_item):
        self.learn_item = learn_item
        
    def getUrl(self):
        return strLearn
    
    def getBody(self):
        return json.dumps({'learn_item':self.learn_item})
    
class Teach(Task):
    def __init__(self,teach_item,val):
        self.teach_item = teach_item
        self.val = val
        
    def getUrl(self):
        return strTeach
    
    def getBody(self):
        return json.dumps({'teach_item':self.teach_item,
                           'val':self.val})
        
def paxos_alive(host,port):
    
    t = Alive()
    mission.execute(t, host, port, 5)
    return t.response

def paxos_learn(host,port,item):
    
    t = Learn(item)
    mission.execute(t, host, port, 5)
    return t.response

def paxos_teach(host,port,item,val):
    t = Teach(item,val)
    mission.execute(t, host, port, 5)
    return t.response

def test():
    pass

if __name__ == '__main__':
#    paxos_alive('127.0.0.1',10011)
    print paxos_learn('127.0.0.1',19011,learn_paxos_leader)
    print paxos_teach('127.0.0.1',19011,teach_paxos_leader,'nSwfsePF-0GHDbc-KJcV')
    