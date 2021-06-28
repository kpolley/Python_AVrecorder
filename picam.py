import time
import os
import sys
from AudioRecorder import AudioRecorder
from VideoRecorder import VideoRecorder


def record_media(rec_time):
    a = time.asctime(time.localtime(time.time()))
    a = a.replace(" ", "-").replace(":", "")
    file_name = a
    
    start_AVrecording(file_name, rec_time)


def start_AVrecording(file_name, rec_time):
    print("Starting threads...")
    video_thread.start(file_name, tmp_dir, rec_time)
    if audio:
        audio_thread.start(file_name, tmp_dir)
        audio_thread.stop(rec_time)


def main():
    global video_thread
    global audio_thread
    global tmp_dir
    global final_dir

    # Creates tmp directory if does not exist
    tmp_dir = os.path.expanduser('~/aa-cam/media/raw_media')
    if not os.path.isdir(tmp_dir):
        print("Can't find tmp media directory, creating...")
        os.mkdir(tmp_dir)

    # Initializes threads
    video_thread = VideoRecorder()
    if audio:
        audio_thread = AudioRecorder()

    # Allows time for camera to boot up
    time.sleep(2)

    print("Recording for " + str(rec_time) + " seconds")
    record_media(rec_time)
    print("Success")


if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            "Arguments incorrect -> {script} {record_time seconds} {audio boolean}"
        else:
            rec_time = int(sys.argv[1])
            if sys.argv[2] == "True":
                audio = True
            elif sys.argv[2] == "False":
                audio = False
    except Exception:
        "Arguments incorrect -> {script} {record_time seconds} {audio boolean}"
    main()
