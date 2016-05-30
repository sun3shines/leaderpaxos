# -*- coding: utf-8 -*-

from leaderpaxos.share.http import jresponse
from leaderpaxos.share.urls import strTest,strLearn
from leaderpaxos.acceptor.httpserver.http_server import doTest,do_paxos_learn

url2view = {}

url2view.update({strTest:doTest})
url2view.update({strLearn:do_paxos_learn})

def process_request(request):
    
    url = request.path
    print url
    if url not in url2view:
        return jresponse('-1','url error',request,404)
     
    return url2view[url](request)
