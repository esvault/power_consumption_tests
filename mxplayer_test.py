from base_test import BaseTest
import subprocess as sp
from time import sleep

class MxPlayerTest(BaseTest):
    def __init__(self, adb_path):
        super(MxPlayerTest, self).__init__(adb_path)
        self.adb = adb_path
        self.package_name = 'com.mxtech.videoplayer.ad'
        self.activity = 'com.mxtech.videoplayer.ad.ActivityWelcomeMX'

    def certain_virtual_test(self, time_sec):
        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.activity}'.split(' ')
        
        _ = sp.check_output(start_app)

        
        select_folder = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 4.3)}'.split(' ')
        select_video = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 6.9)}'.split(' ')
        
        sleep(2)
        _ = sp.check_output(select_folder)
        _ = sp.check_output(select_video)

        sleep(time_sec)
        self.close_recent_app()
        self._kill_app()


if __name__ == "__main__":
    test = MxPlayerTest('adb')
    test.exec_test(20)
    print(test.get_results())