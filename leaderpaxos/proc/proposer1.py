
from leaderpaxos.proc.p import load,iduuid
from leaderpaxos.httpserver.core.run import start

paxos_hosts = [('nSwfsePF-0GHDbc-KJcV','127.0.0.1',10011)]

@iduuid(*paxos_hosts[0],hosts=paxos_hosts)
def pstart(*args,**kwargs):
    load()
    start()

if __name__ == '__main__':

    pstart()

