import os
import winsound


WORKING_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
SOUND_PATH = os.path.join(WORKING_PATH, "resources/sound/")

SND_ACTIVATE = os.path.join(SOUND_PATH, "activate.wav")
SND_DEACTIVATE = os.path.join(SOUND_PATH, "deactivate.wav")
SND_MESSAGE = os.path.join(SOUND_PATH, "message.wav")
SND_ERROR = os.path.join(SOUND_PATH, "error.wav")
SND_WARNING = os.path.join(SOUND_PATH, "warning.wav")
SND_DING = os.path.join(SOUND_PATH, "ding.wav")


def play(sound):
    flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT | winsound.SND_ASYNC
    if not os.path.isfile(sound):
        print("Sound error: File not found '%s'." % sound)
    winsound.PlaySound(sound, flags)


if __name__ == "__main__":
    import time
    play(SND_ACTIVATE)
    time.sleep(3)
    play(SND_DEACTIVATE)
    time.sleep(3)
    play(SND_MESSAGE)
    time.sleep(3)
    play(SND_ERROR)
    time.sleep(3)
    play(SND_WARNING)
    time.sleep(3)
    play(SND_DING)
    time.sleep(3)
