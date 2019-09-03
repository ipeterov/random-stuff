import boto3
import time, datetime


class UtilsManager:

    def __init__(self, master):
        self.master = master
        self.client = boto3.client('ec2')

    def info_on_ec2(self):
        reply = self.client.describe_instances()
        info = {}
        for reservation in reply['Reservations']:
            for instance in reservation['Instances']:
                if 'PublicIpAddress' in instance:
                    info[instance['PublicIpAddress']] = instance
        return info

    def ec2_core_tps(self, chunk_id):
        ec2_cores = {
            'c4.large': 2,
            'c4.xlarge': 4,
            'c4.2xlarge': 8,
            'c4.4xlarge': 16,
            'c4.8xlarge': 36
            }
        nodes_tps = self.master.nodes_tps(chunk_id)
        info = self.info_on_ec2()
        tpss = []
        for node_ip, tps in nodes_tps:
            if node_ip in info and info[node_ip]['InstanceType'] in ec2_cores: # Спот инстанс
                tpss.append(tps / ec2_cores[info[node_ip]['InstanceType']])

        if info:
            return sum(tpss) / len(tpss)
        else:
            # No data for this chunk availible or no EC2 cores
            return None

    def estimate_cores(self, time=3600):
        total_cores = 0
        for chunk_id in self.master.chunks:
            tasks_left = self.master.tasks_left(chunk_id)
            tasks_left -= self.spot_tasks_left(chunk_id, time)
            tasks_left -= self.non_spot_tps(chunk_id) * time
            core_tps = self.ec2_core_tps()
            if core_tps != None:
                total_cores += tasks_left / (core_tps * time)
        return total_cores

    def non_spot_tps(self, chunk_id):
        nodes_tps = self.master.nodes_tps(chunk_id)
        info = self.info_on_ec2()
        non_spot_tps = 0
        for node_ip, tps in nodes_tps:
            if not (node_ip in info and info[node_ip]['InstanceType'] in ec2_compute_cores): # Не спот инстанс
                non_spot_tps += tps
        return non_spot_tps

    def spot_tasks_left(self, chunk_id, time=3600):
        nodes_tps = self.master.nodes_tps(chunk_id)
        info = self.info_on_ec2()
        spot_tl = 0
        for node_ip, tps in nodes_tps:
            if node_ip in info and 'InstanceLifecycle' in info[node_ip] and info[node_ip]['InstanceLifecycle'] == 'spot':
                spot_tl += (time - (datetime.datetime.now(datetime.timezone.utc) - info[node_ip]['LaunchTime']).total_seconds()) * tps
        if spot_tl < 0: spot_tl = 0
        return spot_tl
