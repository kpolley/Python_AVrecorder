from AudioRecorder import AudioRecorder
from VideoRecorder import VideoRecorder
import time
from gpiozero import Button
from signal import pause

def start_AVrecording():
    timestamp = time.time()

    video_thread.start(timestamp)
    audio_thread.start(timestamp)
    time.sleep(10)
    audio_thread.stop()
    video_thread.stop()

def test_audio():
    audio_thread.test()

def main():
    global video_thread
    global audio_thread
    
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()

    # Allows time for camera to boot up
    time.sleep(5)

    button = Button(14)
    button.when_pressed = start_AVrecording
    print("ready for action!")
    pause()

if __name__ == "__main__":
    main()