
from statmachine.httpserver.static import wsgiObj

def machine_key_set(key,val):
    wsgiObj.MACHINE_STATE.put(key, val)

def machine_key_get(key,val):
    return wsgiObj.MACHINE_STATE.get(key)

def machine_key_del(key,val):
    wsgiObj.MACHINE_STATE.pop(key)

def machine_all():
    return wsgiObj.MACHINE_STATE.all()

def machine_load():
    pass
