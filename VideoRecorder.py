import threading
import random
import picamera

class VideoRecorder:
    def __init__(self):
        self.file_name = 'default_name'
        self.camera = picamera.PiCamera()
        self.camera.framerate = 25

    def record(self):
        self.camera.start_recording(self.file_name)

    def stop(self):
        self.camera.stop_recording()

    def start(self, timestamp):
        self.file_name = '{}.h264'.format(timestamp)

        video_thread = threading.Thread(target=self.record)
        video_thread.start()