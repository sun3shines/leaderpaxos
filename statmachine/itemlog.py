
from leaderpaxos.httpclient.libmachine import key_store
from statmachine.httpserver.static import wsgiObj
from leaderpaxos.share.http import http_success

def logstorage(cmd,key,val):
        
    resp = key_store(wsgiObj.leaderHost, wsgiObj.leaderPort, cmd, key, val)
    if not http_success(resp):
        return False,resp.get('msg')
    return True,''
