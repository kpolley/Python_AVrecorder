import threading
import picamera

class VideoRecorder:
    def __init__(self):
        self.open = True
        self.file_name = '{}.h264'.format(timestamp)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 648)

    def record(self):
        self.camera.start_recording(self.file_name)
        while(self.open == True):
            if(self.open == False):
                break

    def stop(self):
        self.camera.stop_recording()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()
        
# class VideoRecorder:
#     def __init__(self, timestamp):
#         self.resolution = (640, 648)
#         self.file_name = '{}.h264'.format(timestamp)
#         self.duration = 10 # seconds
#         self.camera = None

#     def boot_camera(self):
#         self.camera = picamera.PiCamera()
#         self.camera.resolution = self.resolution

#     def record(self):
#         self.camera.start_recording(self.file_name)
#         self.camera.wait_recording(self.duration)
#         self.camera.stop_recording()

#     def start(self):
#         video_thread = threading.Thread(target=self.record)
#         video_thread.start()