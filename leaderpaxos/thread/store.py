# -*- coding: utf-8 -*-

import threading
import traceback
from leaderpaxos.thread.learn import item_proposer_learn
from leaderpaxos.thread.broad import item_proposer_broad
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.uuid import get_vs_uuid as get_broad_uuids
from leaderpaxos.share.signal import getQueuItem,signal_sleep

def log_store(logentry):
    
    logUuid = get_broad_uuids()
    wsgiObj.store_param.put((logUuid,logentry))
    return get_resp(logUuid)

def get_resp(logUuid):

    resp = None    
    while True:
        uuid,data = getQueuItem(wsgiObj, wsgiObj.store_resut)
        if logUuid == uuid:
            resp = data
            break
        else:
            wsgiObj.signalLearn.put((uuid,data))
            signal_sleep(wsgiObj, 0.1)
    return resp

def get_item():
    
    item = 0
    while True:
        keyitem = str(item)
        val = item_proposer_learn(keyitem)
        if not val:
            print 'learn %s as empty item' % (keyitem)
            yield keyitem
        else:
            print 'learn item %s data as %s' % (keyitem,val)
        item = item + 1    
    
def paxos_item_store():

    while True:
        for keyitem in get_item():
            logUuid,logentry = getQueuItem(wsgiObj, wsgiObj.store_param)
            item_proposer_broad(keyitem, logentry, get_broad_uuids())
            wsgiObj.store_resut.put((logUuid,0))

class do_paxos_store(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        try:
            print 'item store thread start'
            paxos_item_store()
        except:
            print traceback.format_exc()
            print 'thread down do_paxos_store'
            pass
            
