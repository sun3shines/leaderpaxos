# -*- coding: utf-8 -*-

import threading

class Base(object):
    
    def __init__(self):
        self.l = []
        self.d = {}
        self.lock = threading.Lock()
        
    def putl(self,val):
        if self.lock.acquire():
            if val not in self.l:
                self.l.append(val)
            self.lock.release()
            
    def rmvl(self,val):
        if self.lock.acquire():
            if val in self.l:
                self.l.remove(val)
            self.lock.release()
            
    def lhas_val(self,val):
        return val in self.l
    
    def dhas_val(self,key):
        return self.d.has_key(key)
    
    def putd(self,key,val):
        if self.lock.acquire():
            self.d.update({key:val})
            self.lock.release()
            
    def getd(self,key):
        return self.d.get(key)
    
    def rmvd(self):
        pass
    
    @property
    def countl(self):
        return len(self.l)
    
    @property
    def countd(self):
        return len(self.d.keys())


    
