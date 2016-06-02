# -*- coding: utf-8 -*-

import json
import time
from leaderpaxos.share.http import jresponse
from statmachine.httpserver.static import wsgiObj


def doTest(request):

    return jresponse('0','test ok',request,200)
    


