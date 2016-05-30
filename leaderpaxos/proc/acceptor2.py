
from leaderpaxos.proc.pa import acceptor_iduuid
from leaderpaxos.acceptor.httpserver.core.run import start


paxos_acceptors = [('jUrSriFq-cCvpHT-NX4e','127.0.0.1',19011),
                   ('kgfVNfTc-jSpDxE-SoTp','127.0.0.1',19012),
                   ('bLwGEq38-DXFTS7-XuBT','127.0.0.1',19013)]

@acceptor_iduuid(*paxos_acceptors[1],acceptors=paxos_acceptors)
def pstart(*args,**kwargs):
    start()

if __name__ == '__main__':

    pstart()
