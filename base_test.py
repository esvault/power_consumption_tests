from freq_statistics import get_idle_freq_statistics, get_idle_freq_delta

import subprocess as sp
from time import time, sleep
import os


class BaseTest:
    def __init__(self, adb_path):
        self.adb = adb_path

        out = sp.check_output(f'{adb_path} shell wm size'.split(' '))
        x_max, y_max = out.decode('utf-8').strip().split(' ')[2].split('x')
        self.x_max = int(x_max)
        self.y_max = int(y_max)

        self.results = []
        self.stats_of_tests = []

        self.package_name = ''

    def _kill_app(self):
        if self.package_name:
            print(f'kill package {self.package_name}')
            sleep(0.3)
            _ = sp.check_output(f'{self.adb} shell am kill {self.package_name}'.split(' '))
            sleep(0.2)
            _ = sp.check_output(f'{self.adb} shell pm disable {self.package_name}'.split(' '))
            _ = sp.check_output(f'{self.adb} shell pm enable {self.package_name}'.split(' '))

    def lock_phone(self):
        _ = sp.check_output(f'{self.adb} shell dumpsys battery reset'.split(' '))
        _ = sp.check_output(f'{self.adb} shell input keyevent KEYCODE_POWER'.split(' '))

    def unlock_phone(self):
        _ = sp.check_output(f'{self.adb} shell dumpsys battery unplug'.split(' '))
        _ = sp.check_output(
            f'{self.adb} shell input keyevent KEYCODE_HOME && input swipe {self.x_max / 2} {3 * self.y_max / 4}'
            f' {self.x_max / 2} {self.y_max / 4} 500'.split(' '))

        self.close_recent_app()

    def close_recent_app(self, need_to_force_out_switch_screen=True):
        """ phone have to be with unlocked screen"""

        _ = sp.check_output(
            f'{self.adb} shell input keyevent KEYCODE_HOME'.split(' '))

        sleep(0.2)
        os.system(f'{self.adb} shell input keyevent KEYCODE_APP_SWITCH')
        sleep(0.2)
        os.system(f'{self.adb} shell input swipe {self.x_max / 2} {int(0.5 * self.y_max)}'
                  f' {self.x_max / 2} {self.y_max / 4} 300')
        sleep(0.2)

        # if smartphone does not close switch screen automatically
        if need_to_force_out_switch_screen:
            os.system(f'{self.adb} shell input keyevent KEYCODE_BACK')

    def certain_virtual_test(self, time_sec):
        print("No test scenario")

    def exec_test(self, time_sec=3):

        # Get freq governor name
        out = sp.check_output(f'{self.adb} shell cat '
                                      f'/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor'.split(' '))
        self.freq_gov_name = out.decode('utf-8').strip()
        self.unlock_phone()

        print(f'Collect data before test...')
        before_time = time()
        stats_freq_before = get_idle_freq_statistics()

        print(f'start test')
        self.certain_virtual_test(time_sec)

        print(f'Collect data after test...')
        stats_freq_after = get_idle_freq_statistics()
        after_time = time()

        diff = get_idle_freq_delta(stats_freq_before, stats_freq_after)

        stat_test = {'test_time(sec)': after_time - before_time}
        self.stats_of_tests.append(stat_test)

        result = {'diff': diff, 'before': stats_freq_before, 'after': stats_freq_after}
        self.results.append(result)

        self.lock_phone()

    def get_results(self):
        return self.results

if __name__ == "__main__":
    test = BaseTest('adb')
    test.package_name = 'net.sourceforge.opencamera'
    test.exec_test()
    print(test.get_results())