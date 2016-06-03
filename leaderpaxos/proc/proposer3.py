# -*- coding: utf-8 -*-

from leaderpaxos.proc.pp import proposer_load,proposer_iduuid
from leaderpaxos.proposer.httpserver.core.run import start

paxos_hosts = [('nswfsepf-0ghdbc-kjcv','127.0.0.1',10011),
               ('usqdvwpq-clikts-trwj','127.0.0.1',10012),
               ('clmf5diw-2fj61w-qinu','127.0.0.1',10013)]

paxos_acceptors = [('jursrifq-ccvpht-nx4e','127.0.0.1',19011),
                   ('kgfvnftc-jspdxe-sotp','127.0.0.1',19012),
                   ('blwgeq38-dxfts7-xubt','127.0.0.1',19013)]

mst_cmds = ['python machine1.py',
            'python machine2.py',
            'python machine3.py']

proc_index = 2
@proposer_iduuid(proc_index,*paxos_hosts[proc_index],hosts=paxos_hosts,
                 acceptors=paxos_acceptors,mst_cmd=mst_cmds[proc_index])

def pstart(*args,**kwargs):
    proposer_load()
    start()

if __name__ == '__main__':

    pstart()
