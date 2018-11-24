import threading
import sounddevice as sd

class AudioRecorder():

    def __init__(self):
        self.fs = 48000
        self.channels = 1
        self.duration = 10

    def record(self):
        sd.rec(int(self.duration * self.fs), samplerate=self.fs, channels=self.channels)
    
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

