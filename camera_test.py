from base_test import BaseTest
from time import time, sleep
import subprocess as sp

class CameraTest(BaseTest):
    def __init__(self, adb_path):
        super(CameraTest, self).__init__(adb_path)

        self.package_name = 'net.sourceforge.opencamera'
        self.activity = 'net.sourceforge.opencamera.MainActivity'

    def certain_virtual_test(self, time_sec):
        start_time = time()

        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.activity}'.split(' ')
        _ = sp.check_output(start_app)
        sleep(4)

        video_start_stop = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 1.1)}'.split(' ')

        _ = sp.check_output(video_start_stop)

        while time() - start_time < time_sec:
            sleep(start_time + time_sec - time())

        _ = sp.check_output(video_start_stop)

        sleep(2)

        self.close_recent_app()

        # delete videos
        _ = sp.check_output(
            f'{self.adb} shell rm -rf /sdcard/DCIM/OpenCamera/*.mp4'.split(' '))

        self._kill_app()

if __name__ == "__main__":
    test = CameraTest('adb')
    test.exec_test(20)
    print(test.get_results())