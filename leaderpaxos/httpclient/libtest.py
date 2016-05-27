
from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 
from leaderpaxos.share.urls import strTest
from leaderpaxos.httpserver.core.static import wsgiObj
class MyTest(Task):
    
    def __init__(self):
        pass
    def getBody(self):
        return ''
    def getUrl(self):
        return strTest


def get_test():
    
    t = MyTest()
    mission.execute(t, wsgiObj.WSGI_HOST, wsgiObj.WSGI_PORT,5)

if __name__ == '__main__':
    get_test()