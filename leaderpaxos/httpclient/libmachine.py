# -*- coding: utf-8 -*-

import json
from leaderpaxos.httpclient.core.task import Task
import leaderpaxos.httpclient.core.mission as mission 

from leaderpaxos.share.urls import strMKeyDel,strMKeySet,strMKeyGet,\
    strMKeyStore,strMSTAGet

class KeySet(Task):
    def __init__(self,key,val):
        self.key = key
        self.val = val
    
    def getUrl(self):
        return strMKeySet
    
    def getBody(self):
        return json.dumps({'key':self.key,
                           'val':self.val})
        
class KeyStore(Task):
    def __init__(self,cmd,key,val):
        self.key = key
        self.val = val
        self.cmd = cmd
        
    def getUrl(self):
        return strMKeyStore
    
    def getBody(self):
        
        logentry = '%s %s' % (self.cmd,self.key)
        if self.val:
            logentry = ' '.join([logentry,self.val]) 
        return json.dumps({'logentry':logentry})
        
class MstGet(Task):
    def getUrl(self):
        return strMSTAGet
    
def key_set(host,port,key,val):
    t = KeySet(key,val)
    mission.execute(t, host, port, 5)
    return t.response

def mst_get(host,port):
    t = MstGet()
    mission.execute(t, host, port, 5)
    return t.response

def key_store(host,port,key,val):
    pass

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 18011

    key_set(host, port, 'test_key', 'test_val')
    mst_get(host, port)
    
   
 
