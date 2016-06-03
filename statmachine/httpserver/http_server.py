# -*- coding: utf-8 -*-

import json
import time
import sys
from leaderpaxos.share.http import jresponse
from statmachine.httpserver.static import wsgiObj
from statmachine.machine_cmd import machine_key_set,machine_key_get,\
    machine_key_del,machine_all,machine_load
from statmachine.itemlog import logstorage
from leaderpaxos.share.urls import ERR_NOT_LEADER

def doTest(request):

    return jresponse('0','test ok',request,200)
    
def doKeySet(request):
    
    param = json.loads(request.body)
    key = param.get('key')
    val = param.get('val')
    
    flag,msg = logstorage('set',key,val)
    
    if not flag:
        if msg == ERR_NOT_LEADER:
            print ERR_NOT_LEADER
            sys.exit(0)
        else:
            return jresponse('-1',msg,request,200)
        
    machine_key_set(key, val)
    
    return jresponse('0','',request,200)

def doKeyGet(request):

    return jresponse('0','test ok',request,200)

def doKeyDel(request):

    return jresponse('0','test ok',request,200)

def doMstGet(request):

    mst = machine_all()
    return jresponse('0',json.dumps(mst),request,200)
