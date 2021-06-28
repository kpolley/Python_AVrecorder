import threading
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
        self.file_name = 'default_name'  # This should be replaces with a value given in self.start()
        self.camera = picamera.PiCamera()
        self.camera.sensor_mode = 2
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 25
        self.camera.rotation = 0
        self.camera.iso = iso
        self.camera.shutter_speed = speed

    def record(self, rec_time):
        self.camera.start_recording(self.file_name)
        self.camera.wait_recording(rec_time)
        self.camera.stop_recording()
        print("Finished video recording")

    def stop(self):
        self.camera.stop_recording()

    def start(self, file_name, file_dir, rec_time):
        self.file_name = '{}/{}.h264'.format(file_dir, file_name)

        video_thread = threading.Thread(target=self.record, args=(rec_time,))
        video_thread.start()
