# -*- coding: utf-8 -*-

from leaderpaxos.proc.pp import proposer_load,proposer_iduuid
from leaderpaxos.proposer.httpserver.core.run import start

paxos_hosts = [('nSwfsePF-0GHDbc-KJcV','127.0.0.1',10011)]

paxos_acceptors = [('jUrSriFq-cCvpHT-NX4e','127.0.0.1',19011),
                   ('kgfVNfTc-jSpDxE-SoTp','127.0.0.1',19012),
                   ('bLwGEq38-DXFTS7-XuBT','127.0.0.1',19013)]

@proposer_iduuid(*paxos_hosts[0],hosts=paxos_hosts,acceptors=paxos_acceptors)
def pstart(*args,**kwargs):
    proposer_load()
    start()

if __name__ == '__main__':

    pstart()

