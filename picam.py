import time
import subprocess
import os
import sys
from AudioRecorder import AudioRecorder
from VideoRecorder import VideoRecorder

def record_media(rec_time):
    a = time.asctime(time.localtime(time.time () ))
    a = a.replace(" ","-").replace(":","")
    file_name = a
    
    start_AVrecording(file_name)
    time.sleep(rec_time)
    stop_AVrecording(file_name)

def start_AVrecording(file_name):
    print("Starting threads...")
    video_thread.start(file_name, tmp_dir)
    audio_thread.start(file_name, tmp_dir)

def stop_AVrecording(file_name):
    print("Stopping threads...")
    audio_thread.stop()
    video_thread.stop()

    print("starting mux...")
    cmd = "ffmpeg -i {1}/{0}.wav -i {1}/{0}.h264 -c:v copy -c:a aac -strict experimental {2}/{0}.mp4".format(file_name, tmp_dir, final_dir)
    subprocess.call(cmd, shell=True)
    print("done")

def main():
    global video_thread
    global audio_thread
    global tmp_dir
    global final_dir

    # Creates tmp directory if does not exist
    tmp_dir = os.path.expanduser('~/aa-cam/media/raw_media')
    if(os.path.isdir(tmp_dir) == False):
        print("Can't find tmp media directory, creating...")
        os.mkdir(tmp_dir)

    # Creates final media directory if does not exist
    final_dir = os.path.expanduser('~/aa-cam/media')
    if(os.path.isdir(final_dir) == False):
        print("Can't find media directory, creating...")
        os.mkdir(final_dir)

    # Initializes threads
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()

    # Allows time for camera to boot up
    time.sleep(2)

    print("recording for " + str(rec_time) + " seconds")
    record_media(rec_time)
    print("finsihing recording")

if __name__ == "__main__":
    rec_time = int(sys.argv[1])
    main()
