import time
import threading
import subprocess
from AudioRecorder import AudioRecorder
from VideoRecorder import VideoRecorder
from gpiozero import Button
from signal import pause

def record_ten_seconds():
    timestamp = time.time()

    start_AVrecording(timestamp)
    time.sleep(10)
    stop_AVrecording(timestamp)

def start_AVrecording(timestamp):
    print("Starting threads...")
    video_thread.start(timestamp)
    audio_thread.start(timestamp)

def stop_AVrecording(timestamp):
    print("Stopping threads...")
    audio_thread.stop()
    video_thread.stop()

    print("starting mux...")
    cmd = "ffmpeg -i {0}.wav -i {0}.h264 -c:v copy -c:a aac -strict experimental {0}.mp4".format(timestamp)
    subprocess.call(cmd, shell=True)
    print("done")

def main():
    global video_thread
    global audio_thread
    
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()

    # Allows time for camera to boot up
    time.sleep(2)

    button = Button(14)
    button.when_pressed = record_ten_seconds
    print("ready for action!")
    pause()

if __name__ == "__main__":
    main()