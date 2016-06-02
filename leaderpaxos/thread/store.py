# -*- coding: utf-8 -*-

from leaderpaxos.thread.learn import item_proposer_learn
def logentry_store(logentry):
    pass

def get_item():
    
    item = 0
    while True:
        keyitem = str(item)
        val = item_proposer_learn(item)
        if not val:
            yield item
        else:
            item = item + 1
    

