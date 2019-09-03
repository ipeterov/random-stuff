from multiserver.jsonsocket import JSONSocket
import time
import json

class Controller:
    def __init__(self, ip='', port=9089):
        self.socket = JSONSocket()
        self.socket.connect()

    def send_task_chunk( args, )
        'Sends a chunks of tasks that use same function but different argsets'
        task = {
            'package_filename': package_filename,
            'package_name': package_name,
            'package_version': package_version,
            'module_name': module_name,
            'function_name': function_name,
            'args_json': json.dumps(args, sort_keys=True)
        }
