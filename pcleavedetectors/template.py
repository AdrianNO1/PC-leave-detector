import time, os, subprocess
from screeninfo import get_monitors
from playsound import playsound

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

sound_file_path = "pcleavedetectorsound.mp3"
temp_txt_path = "pcleavedetectorTemptxt.txt"

def play_sound(file_path):
    player = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', file_path],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)
    return player

def leavingpc_protocol():
    original_volume = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(0.0, None) # max
    
    #playsound(sound_file_path)
    player = play_sound(sound_file_path)
    while player.poll() is None:  # While the sound is still playing
        time.sleep(0.1)  # Wait a bit before checking again
    player.terminate()  # Make sure the process is terminated

    with open(temp_txt_path, "w") as f:
        f.write(r"""textenasd""")
    os.system(temp_txt_path)
    volume.SetMasterVolumeLevel(original_volume, None)


def monitor_countdown(duration):
    start_time = time.time()
    current_monitors = len(get_monitors())

    while time.time() - start_time < duration:
        new_monitors = len(get_monitors())
        if new_monitors < current_monitors:
            leavingpc_protocol()
            break
        else:
            current_monitors = new_monitors
            time.sleep(1)

monitor_countdown(timenasd)