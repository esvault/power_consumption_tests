from audio_test import AudioTest
from hillclimb_test import HillclimbTest
from camera_test import CameraTest
from mxplayer_test import MxPlayerTest
from note_test import NoteTest

from util import calculate_mah_with_idle, check_adb_connection

if __name__ == "__main__":
    adb = 'adb'
    tests = [
        AudioTest(adb), 
        HillclimbTest(adb), 
        CameraTest(adb), 
        MxPlayerTest(adb), 
        NoteTest(adb)
    ]

    results = dict()
    check_adb_connection(adb)
    for test in tests:
        test.exec_test(10)
        results[test.name] = calculate_mah_with_idle(test.get_results()[0]['diff'])

    print(results)
