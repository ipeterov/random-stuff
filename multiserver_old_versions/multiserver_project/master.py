from multiserver.master_lib import Master
import cmd
import master_utils

class MasterShell(cmd.Cmd):

    intro = 'Welcome to the master shell. Type help or ? to list commands.\n'
    prompt = 'Master > '

    def do_tasks_queued(self, arg):
        print(master.tasks.qsize())

    def do_tasks_done_and_waiting(self, arg):
        print(master.results.qsize())

    def do_tasks_at_nodes(self, arg):
        print(master.tasks_at_nodes)

    def do_empty_result_queue(self, arg):
        master.results.clear()
        print('Result queue is now empty.')

    def do_controller(self, arg):
        print(master.controller.address)

    def do_nodes(self, arg):
        print(list(master.node_manager.nodes.keys()))

    def do_ec2_compute_core_tps(self, arg):
        print(utils_manager.ec2_compute_core_tps())

    def do_estimate_cores(self, arg):
        print(utils_manager.estimate_cores())

    def do_non_spot_tps(self, arg):
        print(utils_manager.non_spot_tps())

    def do_spot_tl(self, arg):
        print(utils_manager.spot_tl())

    def do_info_on_ec2(self, arg):
        print(utils_manager.info_on_ec2())

if __name__ == '__main__':
    master = Master(controller_port=9089, manager_port=9090)
    utils_manager = master_utils.UtilsManager(master)
    master.start()

    master_shell = MasterShell()
    master_shell.cmdloop()
