# -*- coding: utf-8 -*-

from leaderpaxos.share.cache.base import Base

class Mydict(Base):
    
    def put(self,key,val):
        return self.putd(key, val)
    
    def has_key(self,key):
        return self.dhas_val(key)
    
    def get(self,key,userval=None):
        val = self.getd(key)
        if not val:
            return userval
        return val