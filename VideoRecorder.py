import threading
import random
import picamera

class VideoRecorder:
    def __init__(self):
        iso = 0
        speed = 0
        while True:  # Ensures camera settings are definitely read before continuing
            try:
                f = open("camera_settings.txt", "r")
                iso = int(f.readline())
                speed = int(f.readline())
                f.close()
            except:
                continue
            break
        self.file_name = 'default_name' # This should be replaces with a value given in self.start()
        self.camera = picamera.PiCamera()
        self.camera.framerate = 25
        self.camera.rotation = 180
        self.camera.iso = iso
        self.camera.shutter_speed = speed

    def record(self):
        self.camera.start_recording(self.file_name)

    def stop(self):
        self.camera.stop_recording()

    def start(self, file_name, file_dir):
        self.file_name = '{}/{}.h264'.format(file_dir, file_name)

        video_thread = threading.Thread(target=self.record)
        video_thread.start()