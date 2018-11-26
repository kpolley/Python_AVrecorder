import threading
import picamera

class VideoRecorder:
    def __init__(self, timestamp):
        self.file_name = '{}.h264'.format(timestamp)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 648)

    def record(self):
        self.camera.start_recording(self.file_name)

    def stop(self):
        self.camera.stop_recording()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()