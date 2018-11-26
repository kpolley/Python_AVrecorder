from .AudioRecorder import AudioRecorder
from .VideoRecorder import VideoRecorder
import time

def start_AVrecording(filename):
    video_thread = VideoRecorder(timestamp)
    audio_thread = AudioRecorder(timestamp)

def main():
    timestamp = time.time()


    time.sleep(5)
    video_thread.start()
    audio_thread.start()

if __name__ == "__main__":
    main()