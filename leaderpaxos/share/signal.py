# -*- coding: utf-8 -*-

import os
import time

QUEUE_TIMEOUT_INTERVAL = 3
SLEEP_INTERVAL = 1

def signal_handler(obj):
    if obj.interruptEvent.isSet():  
        print 'thread finished'  
        raise KeyboardInterrupt
       
def signal_sleep(obj,seconds):
    
    total = 0
    while total <= seconds:
        signal_handler(obj)
        time.sleep(SLEEP_INTERVAL)
        total = total + SLEEP_INTERVAL
        
def getQueuItem(obj,queue):
    
    while True:
        try:
            item = queue.get(timeout=QUEUE_TIMEOUT_INTERVAL)
        except:
            signal_handler(obj)
        else:
            break    
    return item
