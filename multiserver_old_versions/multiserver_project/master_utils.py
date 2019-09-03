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

    def ec2_compute_core_tps(self):
        ec2_compute_cores = {
            'c4.large': 2,
            'c4.xlarge': 4,
            'c4.2xlarge': 8,
            'c4.4xlarge': 16,
            'c4.8xlarge': 36
            }
        nodes_tps = self.master.nodes_tps()
        info = self.info_on_ec2()
        tpss = []
        for node_ip, tps in nodes_tps:
            if node_ip in info and info[node_ip]['InstanceType'] in ec2_compute_cores:
                tpss.append(tps / ec2_compute_cores[info[node_ip]['InstanceType']])
        if info:
            return sum(tpss) / len(tpss)
        else:
            return None


    def estimate_cores(self):
        tl = self.master.tasks_left()
        tl -= spot_tl()
        tl -= non_spot_tps() * 3600
        core_tph = ec2_compute_core_tps() * 3600
        return tl / core_tph

    def non_spot_tps(self):
        nodes_tps = self.master.nodes_tps()
        info = self.info_on_ec2()
        non_spot_tps = 0
        for node_ip, tps in nodes_tps:
            if (node_ip in info and ('InstanceLifecycle' not in info[node_ip] or info[node_ip]['InstanceLifecycle'] != 'spot')) or node_ip not in info:
                non_spot_tps += tps
        return non_spot_tps

    def spot_tl(self):
        nodes_tps = self.master.nodes_tps()
        info = self.info_on_ec2()
        spot_tl = 0
        for node_ip, tps in nodes_tps:
            if node_ip in info and 'InstanceLifecycle' in info[node_ip] and info[node_ip]['InstanceLifecycle'] == 'spot':
                spot_tl += (3600 - (datetime.datetime.now(datetime.timezone.utc) - info[node_ip]['LaunchTime']).total_seconds()) * tps
        if spot_tl < 0: spot_tl = 0
        return spot_tl
