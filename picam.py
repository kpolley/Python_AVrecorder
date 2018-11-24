from .AudioRecorder import AudioRecorder
from .VideoRecorder import VideoRecorder
import time

def main():
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()

    # Boot up the camera
    video_thread.boot_camera()
    time.sleep(5)

    video_thread.start()
    audio_thread.start()

if __name__ == "__main__":
    main()