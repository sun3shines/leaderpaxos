# -*- coding: utf-8 -*-

from leaderpaxos.share.http import jresponse
from leaderpaxos.share.urls import strTest,strMKeyGet,strMKeySet,strMKeyDel,strMSTAGet
from statmachine.httpserver.http_server import doTest,doKeyDel,doKeyGet,doKeySet,doMstGet

url2view = {}

url2view.update({strTest:doTest})
url2view.update({strMKeyDel:doKeyDel})
url2view.update({strMKeyGet:doKeyGet})
url2view.update({strMKeySet:doKeySet})
url2view.update({strMSTAGet:doMstGet})

def process_request(request):
    
    url = request.path
    if url not in url2view:
        return jresponse('-1','url error',request,404)
     
    return url2view[url](request)
