import subprocess as sp
from util import check_adb_connection, get_cores_amount

# Scaling available governors
#
# ondemand userspace powersave performance 
# darkutil energy-dcfc alucardsched darknesssched 
# smurfutil helix_schedutil pixutil electroutil pwrutilx schedutilX blu_schedutil schedutil

class GovernorSwitcher:
    def __init__(self, path_to_adb): 
        self.adb = path_to_adb

    # return first cores from clusters
    def _get_clusters_cores(self):
        result = []
        cores_amount = get_cores_amount(self.adb)

        core_i = 0
        while core_i < cores_amount:
            command = f'{self.adb} shell cat /sys/devices/system/cpu/cpu{core_i}/cpufreq/related_cpus'
            out = sp.check_output(command.split(' ')).decode('utf-8')
            cluster_cores = list(map(lambda x: int(x), out.strip().split(' ')))
            result.append(core_i)

            core_i = max(cluster_cores) + 1
            
        return result

    def switch(self, governor):
        check_adb_connection('adb')
        
        clusters_cores = self._get_clusters_cores()
        for core_i in clusters_cores:
            command = f'{self.adb} shell echo {governor} > /sys/devices/system/cpu/cpu{core_i}/cpufreq/scaling_governor'
            _ = sp.check_output(command.split(' '))


if __name__ == "__main__":
    gov_switcher = GovernorSwitcher('adb')
    gov_switcher.switch('schedutil')