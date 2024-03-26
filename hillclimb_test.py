from base_test import BaseTest

import subprocess as sp
from time import time, sleep

class HillclimbTest(BaseTest):
    def __init__(self, adb_path):
        super(HillclimbTest, self).__init__(adb_path)
        self.adb = adb_path
        self.package_name = 'com.fingersoft.hillclimb'
        self.activity = 'com.fingersoft.game.MainActivity'

    def certain_virtual_test(self, time_sec):
        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.activity}'.split(' ')
        
        _ = sp.check_output(start_app)
        sleep(10)

        start_game = f'{self.adb} shell input tap {int(self.y_max / 1.33)} {int(self.x_max / 1.35)}'.split(' ')
        _ = sp.check_output(start_game)

        gas_btn = f'{self.adb} shell input swipe {int(self.y_max / 1.1)} {int(self.x_max / 2)} ' \
                  f'{int(self.y_max / 1.1)} {int(self.x_max / 2)} 2000'.split(' ')
        
        brake_btn = f'{self.adb} shell input swipe {int(self.y_max * 0.1)} {int(self.x_max / 2)} ' \
                     f'{int(self.y_max * 0.1)} {int(self.x_max / 2)} 100'.split(' ')

        start_time = time()
        while time() - start_time < time_sec:
            _ = sp.check_output(gas_btn)
            _ = sp.check_output(brake_btn)

        self.close_recent_app()
        self._kill_app()


if __name__ == "__main__":
    test = HillclimbTest('adb')
    test.exec_test(20)
    print(test.get_results())
