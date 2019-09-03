import multiserver
import time
import math

print('Starting multiserver node...')

def longlen(obj):
    time.sleep(5)
    return len(obj)

node = multiserver.Node(longlen, '168.235.86.179', 9090)
node.start()
