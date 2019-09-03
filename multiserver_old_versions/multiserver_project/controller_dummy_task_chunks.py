from multiserver.jsonsocket import JSONSocket
import time
import json

package_filename = 'foo-1.1-py3-none-any.whl'
package_name = 'foo'
package_version = '1.1'
module_name = 'foo_module'
function_name = 'bar'
args = []

def test(num=10, ip=''):

    socket = JSONSocket()
    socket.connect(ip, 9089)

    t = time.perf_counter()

    for _ in range(num):

        task = {
            'package_filename': package_filename,
            'package_name': package_name,
            'package_version': package_version,
            'module_name': module_name,
            'function_name': function_name,
            'args_json': json.dumps(args, sort_keys=True)
        }

        socket.send(task)

    for _ in range(num):
        print(socket.receive())

    print(time.perf_counter() - t)

test(ip='', num = 10)
