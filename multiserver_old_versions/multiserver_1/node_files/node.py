import multiserver
import time
import process1

print('Starting multiserver node.')

node = multiserver.Node(process1.process, 9090)
node.start()
