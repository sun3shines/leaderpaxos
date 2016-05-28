# -*- coding: utf-8 -*-

import os
import time

from leaderpaxos.httpserver.static import wsgiObj,SLEEP_INTERVAL

def signal_handler():
    if wsgiObj.interruptEvent.isSet():  
        print 'thread finished'  
        raise KeyboardInterrupt
       
def signal_sleep(seconds):
    
    total = 0
    while total <= seconds:
        signal_handler()
        time.sleep(SLEEP_INTERVAL)
        total = total + SLEEP_INTERVAL
        
