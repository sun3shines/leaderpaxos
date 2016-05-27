# -*- coding: utf-8 -*-

import os.path
import random


def get_num_random(num=1):
    
    return "".join(random.sample([str(x) for x in range(0,10)],num))

def init_vm_op_uuid():
    
    return get_num_random(8) + "-" + \
           get_num_random(4) + "-" + \
           get_num_random(4) + "-" + \
           get_num_random(4) + "-" + \
           get_num_random(8) + get_num_random(4)

def get_random_word(num=1):

    def init_random(num):
        return ''.join(random.sample([chr(i) for i in range(97, 122)]+[ chr(i) for i in range(48, 57)]+[chr(i) for i in range(65, 90)], num))

    strs = ""
    while num > 0:
        if num >= 3:
            strs = strs + init_random(3)
        else:
            strs = strs + init_random(num)
            break
        num = num - 3
    
    return strs

def get_uuid():

    new_uuid = chr(random.randrange(97,122)) + get_random_word(7) + "-" + get_random_word(6) + "-" + get_random_word(4)

    #temporarily we make sure the first 4 chars of new_uuid is non-number char
    num_chars = ['0','1','2','3','4','5','6','7','8','9']
    len_new_uuid = len(new_uuid)
    array_uuid = []
    i = 0
    num = ord("a")
    while i < len_new_uuid:
        if (new_uuid[i] in num_chars) and (i < 4):
            array_uuid.append(chr(num + int(new_uuid[i])))
            i = i + 1
            continue
        array_uuid.append(new_uuid[i])
        i = i + 1    
    return "".join(array_uuid)

def get_vs_uuid():

    vs_uuid = get_uuid()
    return vs_uuid
    
def loadUuid():
    HOST_PATH = ''
    if not os.path.exists(HOST_PATH):
        uuid = get_vs_uuid()
        with open(HOST_PATH,'w') as f:
            f.write(uuid)
            
    with open(HOST_PATH,'r') as f:
        return f.read()

if __name__ == '__main__':
    print get_vs_uuid()
