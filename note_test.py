from base_test import BaseTest
import subprocess as sp
from time import time, sleep

class NoteTest(BaseTest):
    def __init__(self, adb_path):
        super(NoteTest, self).__init__(adb_path)
        self.name = 'type_test'
        self.package_name = 'com.appmindlab.nano'
        self.activity = 'com.appmindlab.nano.IntroActivity'

    def certain_virtual_test(self, time_sec):
        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n' \
                    f'{self.package_name}/{self.activity}'.split(' ')
        
        _ = sp.check_output(start_app)

        create_note = f'{self.adb} shell input tap {int(self.x_max / 1.1)} {int(self.y_max / 1.1)}'.split(' ')

        type_letter = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 1.3)}'.split()

        sleep(2)
        _ = sp.check_output(create_note)
        start_time = time()

        while time() - start_time < time_sec:
            _ = sp.check_output(type_letter)
            sleep(0.05)

        self.close_recent_app()
        self._kill_app()


if __name__ == "__main__":
    test = NoteTest('adb')
    test.exec_test(10)
    print(test.get_results())