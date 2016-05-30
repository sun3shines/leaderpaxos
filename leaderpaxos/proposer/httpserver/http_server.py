# -*- coding: utf-8 -*-

import json
from leaderpaxos.share.http import jresponse
from leaderpaxos.proposer.httpserver.static import wsgiObj
def doTest(request):

	return jresponse('0','test ok',request,200)

def do_paxos_alive(request):
	
	return jresponse('0',wsgiObj.hostUuid,request,200)