
import time

def get_item():
    item = 0
    while True:
        if item % 3:
            yield item
        item = item +1 


def get_while():

    while True:
        return 'aa'
if __name__ == '__main__':

    print get_while()

    for item in get_item():
        print item
        time.sleep(1)

#    f = get_item()
#    while True:
#        item = f.next()
