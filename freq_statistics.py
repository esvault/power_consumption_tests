import subprocess as sp
from util import get_cores_amount, check_adb_connection

adb_path = 'adb'
path_on_pc = 'C:\\diploma\\apks\\root-checker-6-5-3.apk'
path_on_device = '/sdcard/Download/phoneFiles'

# out = subprocess.check_output(f'{adb_path} devices'.split(' ')).decode('utf-8')
# print(out)

# _ = subprocess.check_output(f'{adb_path} push {path_on_pc} {path_on_device}'.split(' '))

def get_idle_states_amount(core_n):
    out = sp.check_output(f'{adb_path} shell cd /sys/devices/system/cpu/cpu{core_n}/cpuidle && ls | grep state'.split(' ')).decode('utf-8')
    out = out.replace('\r', '').strip().split('\n')

    return len(out)

# Возвращает словарь: {индекс ядра} --> {словарь состояний простоя}
# Словарь состояний простоя: {индекс состояния} --> {время, проведенное в этом состоянии}
def get_idle_time(core):
    result = dict()

    states_amount = get_idle_states_amount(core)

    for state in range(0, states_amount):
        command = f'{adb_path} shell cat /sys/devices/system/cpu/cpu{core}/cpuidle/state{state}/time'
        out = sp.check_output(command.split(' ')).decode('utf-8')
        time = int(out.strip())
        result[state] = time

    return result

# Возвращает словарь: {частота} --> {время, проведенное на этой частоте}
def get_cluster_freq(core):
    result = dict()

    command = f'{adb_path} shell cat /sys/devices/system/cpu/cpu{core}/cpufreq/stats/time_in_state'
    out = sp.check_output(command.split(' ')).decode('utf-8')
    freqs = out.strip().split('\n')

    for freq in freqs:
        data = freq.strip().split(' ')
        result[int(data[0])] = int(data[1])

    return result


def get_idle_freq_statistics():
    result = {'idle': dict(), 'freq': list()}

    cores_amount = get_cores_amount('adb')

    core_i = 0
    next_cluster = core_i

    while core_i < cores_amount:
        idle_time = get_idle_time(core_i)
        result['idle'][core_i] = idle_time

        if core_i == next_cluster:

            out = sp.check_output(
                    f'{adb_path} shell cat /sys/devices/system/cpu/cpu{core_i}/cpufreq/related_cpus'.split(' '))

            related_cpus = list(map(lambda cpu_s: int(cpu_s), out.decode('utf-8').strip().split(' ')))
            next_cluster = max(related_cpus) + 1

            cluster_freq_data = get_cluster_freq(core_i)
            result_full_cluster = {'start_core': core_i, 'end_core': max(related_cpus), 'data': cluster_freq_data}

            result['freq'].append(result_full_cluster)

        core_i += 1

    return result

def get_idle_freq_delta(before, after):
    delta = {'idle': {}, 'freq': []}

        # Freq diff
    for i in range(0, len(after['freq'])):
        cluster_freq = {'start_core': after['freq'][i]['start_core'],
                            'end_core': after['freq'][i]['end_core'],
                            'data': {}}

        for freq in after['freq'][i]['data'].keys():
            cluster_freq['data'][freq] = after['freq'][i]['data'][freq] - before['freq'][i]['data'][freq]

        delta['freq'].append(cluster_freq)

    # Idle diff
    for core in after['idle'].keys():
        delta['idle'][core] = dict()

        for state in after['idle'][core].keys():
            delta['idle'][core][state] = after['idle'][core][state] - before['idle'][core][state]

    return delta

if __name__ == "__main__":
    # print_core_dict(get_freq())
    # print_core_dict(get_idle_time())
    # print(get_cluster_freq(0))
    # print(get_idle_time(0))
    check_adb_connection(adb_path)
    print(get_idle_freq_statistics())