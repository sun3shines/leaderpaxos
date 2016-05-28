
from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 
from leaderpaxos.share.urls import strAlive

class Alive(Task):
    def __init__(self):
        pass
    def getBody(self):
        return ''
    def getUrl(self):
        return strAlive

def paxos_alive(host,port):
    t = Alive()
    mission.execute(t, host, port, 5)
    print t.response

def test():
    pass

if __name__ == '__main__':
    import pdb;pdb.set_trace()
    paxos_alive('127.0.0.1',10011)
