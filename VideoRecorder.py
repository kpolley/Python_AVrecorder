import threading
import picamera

class VideoRecorder():
    def __init__(self):
        self.resolution = (640, 648)
        self.file_name = 'my_video.h264'
        self.duration = 10 # seconds
        self.camera = None

    def boot_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.resolution

    def record(self):
        self.camera.start_recording(self.file_name)
        self.camera.wait_recording(self.duration)
        self.camera.stop_recording()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()