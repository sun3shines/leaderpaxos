# -*- coding: utf-8 -*-

from leaderpaxos.proc.pa import acceptor_iduuid,acceptor_load
from leaderpaxos.acceptor.httpserver.core.run import start
from leaderpaxos.thread.acceptor import acceptor_broadcast
from leaderpaxos.share.urls import key_paxos_leader

paxos_acceptors = [('jursrifq-ccvpht-nx4e','127.0.0.1',19011),
                   ('kgfvnftc-jspdxe-sotp','127.0.0.1',19012),
                   ('blwgeq38-dxfts7-xubt','127.0.0.1',19013),
                   ('aceFEq38-wXFTS7-XuBT','127.0.0.1',19014)]

@acceptor_iduuid(*paxos_acceptors[3],acceptors=paxos_acceptors)
def pstart(*args,**kwargs):
    acceptor_load()
    

if __name__ == '__main__':
    pstart()
    acceptor_broadcast(key_paxos_leader, 'aaaa', 'bbb')
    
