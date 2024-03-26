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
        