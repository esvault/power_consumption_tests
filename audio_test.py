from base_test import BaseTest
from time import time, sleep
import subprocess as sp

class AudioTest(BaseTest):
    def __init__(self, adb_path):
        super(AudioTest, self).__init__(adb_path)
        self.name = 'audio_tests'
        self.package_name = 'com.aimp.player'
        self.activity = 'com.aimp.player.ui.activities.main.MainActivity'

    def certain_virtual_test(self, time_sec):

        start_app = f'{self.adb} shell am start -a android.intent.action.MAIN -n ' \
                    f'{self.package_name}/{self.activity}'.split(' ')
        
        _ = sp.check_output(start_app)

        play_stop_music = f'{self.adb} shell input tap {int(self.x_max / 2)} {int(self.y_max / 1.17)}'.split(' ')

        sleep(1)
        _ = sp.check_output(play_stop_music)
        sleep(time_sec)
        _ = sp.check_output(play_stop_music)

        self.close_recent_app()
        self._kill_app()

if __name__ == "__main__":
    test = AudioTest('adb')
    test.exec_test(10)
    print(test.get_results())