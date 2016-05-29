

from leaderpaxos.httpclient.libpaxos import paxos_alive
from leaderpaxos.share.http import http_success
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.share.signal import signal_sleep

def paxos_state(host,port,hostUuid):
    
    while True:
        
        resp = paxos_alive(host, port)
        if http_success(resp) and hostUuid.lower() == resp.get('msg','').lower():
            wsgiObj.PAXOS_STATE.put(hostUuid,True)
        else:
            wsgiObj.PAXOS_STATE.put(hostUuid,False)
        signal_sleep(2)
        
def display_state():
    
    while True:
        
        for hostUuid,_,_ in wsgiObj.PAXOS_HOSTS:
            if hostUuid == wsgiObj.hostUuid:
                continue
            print hostUuid,wsgiObj.PAXOS_STATE.get(hostUuid,False)
        signal_sleep(3)
        
