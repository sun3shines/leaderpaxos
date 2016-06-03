# -*- coding: utf-8 -*-

from statmachine.proc.pm import machine_iduuid,machine_load

from statmachine.httpserver.core.run import start


machine_hosts = [('nswfsepf-0ghdbc-kjcv','127.0.0.1',18011),
               ('usqdvwpq-clikts-trwj','127.0.0.1',18012),
               ('clmf5diw-2fj61w-qinu','127.0.0.1',18013)]

proposer_hosts = [('nswfsepf-0ghdbc-kjcv','127.0.0.1',10011),
               ('usqdvwpq-clikts-trwj','127.0.0.1',10012),
               ('clmf5diw-2fj61w-qinu','127.0.0.1',10013)]

@machine_iduuid(*machine_hosts[2],proposer_hosts[2])
def pstart(*args,**kwargs):
    machine_load()
    start()

if __name__ == '__main__':
    pstart()
