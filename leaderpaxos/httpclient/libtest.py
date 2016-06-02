# -*- coding: utf-8 -*-

from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 
from leaderpaxos.share.urls import strTest

class MyTest(Task):
    
    def __init__(self):
        pass
    def getBody(self):
        return ''
    def getUrl(self):
        return strTest


def get_test(host,port):
    
    t = MyTest()
    mission.execute(t, host,port,5)
    print t.response

if __name__ == '__main__':
#    get_test('127.0.0.1',10011)
#    get_test('127.0.0.1',19011)
    get_test('127.0.0.1',18011)
