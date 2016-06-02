# -*- coding: utf-8 -*-

import json
from leaderpaxos.share.http import jresponse
from leaderpaxos.proposer.httpserver.static import wsgiObj
from leaderpaxos.thread.identity import is_leader
from leaderpaxos.share.urls import ERR_NOT_LEADER
def doTest(request):

	return jresponse('0','test ok',request,200)

def do_paxos_alive(request):
	
	param = json.loads(request.body)
	clientUuid = param.get('clientUuid')
	return jresponse('0',wsgiObj.hostUuid,request,200)

def do_mkey_store(request):
	
	if not is_leader():
		return jresponse('-1',ERR_NOT_LEADER,request,200)
	
	param = json.loads(request.body)
	logentry = param.get('logentry')
	
	return jresponse('0','',request,200)