
import json
from leaderpaxos.httpserver.core.http import jresponse

def doTest(request):
    
    return jresponse('0','test ok',request,200)

