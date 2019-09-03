from multiserver.controller_lib import Controller

import cmd


class ControllerShell(cmd.Cmd):

    intro = 'Welcome to the controller shell. Type help or ? to list commands.\n'
    prompt = 'Controller > '

    def do_master(self, arg):
        print(controller.master_connection.server_address)

    def do_connect_to_some_master(self, arg):
        print(controller.master_connection.assure_that_connected())

    def do_wait_for_chunk(self, arg):
        chunk_id = arg.split()[0]
        controller.wait_for_chunk_completion(chunk_id)
        print('Chunk completed')

    def do_get_result_from_db(self, arg):
        chunk_id = arg.split()[0]
        print(controller.get_results_from_db())

    def do_send_test_chunk_and_get_result_from_db(self, arg):
        argslists = [[] for i in range(10)]
        chunk_id, task_ids = controller.send_task_chunk('foo-1.2-py3-none-any.whl', 'foo', '1.2', 'foo_module', 'bar', argslists)
        print(chunk_id)
        controller.wait_for_chunk_completion(chunk_id)
        results = controller.get_results_from_db(chunk_id)
        print(results)

if __name__ == '__main__':

    controller = Controller()

    controller_shell = ControllerShell()
    controller_shell.cmdloop()
