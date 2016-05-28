
from leaderpaxos.share.cache.base import Base
class Mylist(Base):
    
    def put(self,val):
        return self.putl(val)
    
    def has_val(self,val):
        return self.lhas_val(val)
