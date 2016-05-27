# -*- coding: utf-8 -*-

from leaderpaxos.httpserver.core.http import jresponse
from leaderpaxos.share.urls import strTest
from leaderpaxos.httpserver.http_server import doTest

url2view = {}

url2view.update({strTest:doTest})

def process_request(request):
    
    url = request.path
    print url
    if url not in url2view:
        return jresponse('-1','url error',request,404)
     
    return url2view[url](request)
