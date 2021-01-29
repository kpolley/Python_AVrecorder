import threading
import random
from picamera import PiCamera, Color
import datetime
from time import sleep

class VideoRecorder:
    def __init__(self):
        self.file_name = 'default_name' # This should be replaces with a value given in self.start()
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 25
        self.camera.rotation = 0 #180

    def record(self):
        self.camera.start_recording(self.file_name)

        annotate_thread = threading.Thread(target=self.update_annotation)
        annotate_thread.start()

    def stop(self):
        self.camera.stop_recording()

    def update_annotation(self):
        while self.camera.recording:
            self.camera.annotate_background = Color('blue')
            self.camera.annotate_foreground = Color('yellow')
            self.camera.annotate_text = datetime.datetime.now().strftime("%Y%m%d, %H:%M:%S")
            self.camera.annotate_text_size = 20
            sleep(1)            

    def start(self, file_name, file_dir):
        self.file_name = '{}/{}.h264'.format(file_dir, file_name)

        video_thread = threading.Thread(target=self.record)
        video_thread.start()