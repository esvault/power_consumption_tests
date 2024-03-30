import subprocess as sp
from time import sleep

def get_cores_amount(adb_path):
    out = sp.check_output(f'{adb_path} shell cd /sys/devices/system/cpu && ls | grep cpu'.split(' ')).decode('utf-8')
    out = out.replace("\r", "").split('\n')

    cpu_units = list(filter(lambda x: x[3:].isnumeric() and len(x) > 0, out))

    return len(cpu_units)


def check_adb_connection(adb_path):
        root_cmd = f'{adb_path} root'.split(' ')
        shell_exit_cmd = f'{adb_path} shell exit'.split(' ')

        try:
            _ = sp.check_output(root_cmd)
            sleep(0.5)
            _ = sp.check_output(shell_exit_cmd)

        except sp.CalledProcessError as e:
            print("Can not connect Via adb to device\n"
                  f"command: <{e.cmd}> did not executed successfully")
            raise Exception(f"Can not connect Via adb to device, did not execute <{e.cmd}>")

clusters = [[0, 1, 2, 3, 4, 5], [6, 7]]

power_constants = {
     0: {
          2000000: 90.04,
          1933000: 85.8,
          1866000: 80.27,
          1800000: 72.77,
          1733000: 66.61,
          1666000: 62.05,
          1618000: 58.95,
          1500000: 52.33,
          1375000: 44.83,
          1275000: 39.69,
          1175000: 35.5,
          1075000: 31.24,
          975000:  27.86,
          875000:  25,
          774000:  23.5,
          500000:  19.55
     },
     1: {
          2050000: 324.33,
          1986000: 307.98,
          1923000: 291.52,
          1860000: 269.61,
          1796000: 247.53,
          1733000: 233.56,
          1670000: 209.73,
          1530000: 177.39,
          1419000: 152.46,
          1308000: 130.33,
          1169000: 105.19,
          1085000: 91.11,
          1002000: 79.53,
          919000:  70.65,
          835000:  61.38,
          774000:  56.85

     }
}

available_freqs = {
     0: power_constants[0].keys(),
     1: power_constants[1].keys()
}

def calculate_mah(statistics_dict):
    idle = statistics_dict['idle']
    freq = statistics_dict['freq']

    power_cons = 0
    for cluster_i in range(0, len(clusters)):
        
        for f in available_freqs[cluster_i]:
             power_cons += freq[cluster_i]['data'][f] * power_constants[cluster_i][f] * len(clusters[cluster_i])
         

    return float("%.3f" % (power_cons / float(3600 * 100)))

def calculate_mah_with_idle(statistics_dict):
    idle = statistics_dict['idle']
    freq = statistics_dict['freq']

    power_consumption = 0
    for cluster_i in range(0, len(clusters)):
        time_sum = float(sum(freq[cluster_i]['data'].values()))

        for core_i in clusters[cluster_i]:
            for f in freq[cluster_i]['data'].keys():
                time_precent = freq[cluster_i]['data'][f] / time_sum

                freq_time = freq[cluster_i]['data'][f] - (float(idle[core_i][1]) / 1_0_000.0) * time_precent

                if freq_time < 0:
                    freq_time = 0

                power_consumption += freq_time * power_constants[cluster_i][f]

    return float('%.3f' % (power_consumption / float(3600 * 100)))