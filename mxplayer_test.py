from base_test import BaseTest
import subprocess as sp
from time import sleep

class MxPlayerTest(BaseTest):
    def __init__(self, adb_path):
        super(MxPlayerTest, self).__init__(adb_path)
        self.name = 'video_test'
        self.package_name = 'com.mxtech.videoplayer.ad'
        self.activity = 'com.mxtech.videoplayer.ad.ActivityWelcomeMX'

    def certain_virtual_test(self, time_sec):
        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.activity}'.split(' ')
        
        _ = sp.check_output(start_app)
        sleep(2)

        self._skip_welcome_activity()
        sleep(1)

        select_folder = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 4.3)}'.split(' ')
        select_video = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 6.9)}'.split(' ')
        
        _ = sp.check_output(select_folder)
        _ = sp.check_output(select_video)

        sleep(time_sec)
        self.close_recent_app()
        self._kill_app()

    def _skip_welcome_activity(self):
        select_location = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 3.21)}'.split(' ')
        confirm = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 2)}'.split(' ')

        _ = sp.check_output(select_location)
        sleep(0.2)
        _ = sp.check_output(confirm)


if __name__ == "__main__":
    test = MxPlayerTest('adb')
    test.exec_test(20)
    print(test.get_results())