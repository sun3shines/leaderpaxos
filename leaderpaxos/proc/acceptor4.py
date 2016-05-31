# -*- coding: utf-8 -*-

from leaderpaxos.proc.pa import acceptor_iduuid,acceptor_load
from leaderpaxos.acceptor.httpserver.core.run import start
from leaderpaxos.thread.acceptor import acceptor_broadcast
from leaderpaxos.share.urls import broad_paxos_leader

paxos_acceptors = [('jUrSriFq-cCvpHT-NX4e','127.0.0.1',19011),
                   ('kgfVNfTc-jSpDxE-SoTp','127.0.0.1',19012),
                   ('bLwGEq38-DXFTS7-XuBT','127.0.0.1',19013),
                   ('aceFEq38-wXFTS7-XuBT','127.0.0.1',19014)]

@acceptor_iduuid(*paxos_acceptors[3],acceptors=paxos_acceptors)
def pstart(*args,**kwargs):
    acceptor_load()
    

if __name__ == '__main__':
    import pdb;pdb.set_trace()
    pstart()
    acceptor_broadcast(broad_paxos_leader, 'aaaa', 'bbb')
    
