
from leaderpaxos.httpclient.libmachine import key_set,mst_get

def get_logs():
    path = 'logs.txt'
    cmds = []
    with open(path,'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            elms = line.split()
            if len(elms) != 3:
                continue
            cmds.append(tuple(elms))
    return cmds


if __name__ == '__main__':
    import pdb;pdb.set_trace()
    host = '127.0.0.1'
    port = 18011    
    for c,key,val in  get_logs():
        resp = key_set(host, port, key, val)
        if '0' != resp.get('status'):
            print resp
            break
        
    print mst_get(host, port)
    
