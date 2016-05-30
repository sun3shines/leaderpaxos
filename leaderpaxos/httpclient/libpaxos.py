
import json
from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 
from leaderpaxos.share.urls import strAlive,strLearn
from leaderpaxos.share.urls import learn_paxos_leader

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
    
def paxos_alive(host,port):
    t = Alive()
    mission.execute(t, host, port, 5)
    return t.response

def paxos_learn(host,port,item):
    t = Learn(item)
    mission.execute(t, host, port, 5)
    return t.response

def test():
    pass

if __name__ == '__main__':
#    paxos_alive('127.0.0.1',10011)
    print paxos_learn('127.0.0.1',19011,learn_paxos_leader)
