from multiserver.node_lib import Node
import time
import boto3
import json
import cmd

class NodeShell(cmd.Cmd):

    intro = 'Welcome to the node shell. Type help or ? to list commands.\n'
    prompt = 'Node > '

    def do_process_count(self, arg):
        print(len(node.processes))

    def do_master(self, arg):
        print(node.master_connection.server_address)

    def do_amazon(self, arg):
        if node.is_amazon:
            print('This is Amazon EC2 instance. ID is {}, type is {}.'.format(node.instance_id, node.instance_type))
        else:
            print('This is not an Amazon EC2 instance.')

    def do_stop(self, arg):
        print('Stopping node...')
        node.stop()
        print('Stopped.')

    def do_master_addresses(self, arg):
        print(node.master_connection.node_config['master_addresses'])


if __name__ == '__main__':

    client = boto3.client('s3')

    node_config = json.loads(open('./node_config.json').read())
    node_config.update(json.loads(client.get_object(Bucket='ipeterov', Key='node_config.json')['Body'].read().decode("utf-8")))

    master_address = node_config['master_addresses'][node_config['current_master']]

    node = Node(master_address=master_address, process_count=None)
    node.start()

    node_shell = NodeShell()
    node_shell.cmdloop()
