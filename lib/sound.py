import os
import winsound


WORKING_PATH = os.path.split(os.getcwd())[0]
SOUND_PATH = os.path.join(WORKING_PATH, "resources/sound/")
NOTIFY_ACTIVATE = os.path.join(SOUND_PATH, "activate.wav")
NOTIFY_DEACTIVATE = os.path.join(SOUND_PATH, "deactivate.wav")
NOTIFY_MESSAGE = os.path.join(SOUND_PATH, "message.wav")


def play(sound):
    flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT | winsound.SND_ASYNC
    winsound.PlaySound(sound, flags)


if __name__ == "__main__":
    import time
    play(NOTIFY_ACTIVATE)
    time.sleep(2)
    play(NOTIFY_DEACTIVATE)
    time.sleep(2)
    play(NOTIFY_MESSAGE)
    time.sleep(2)
