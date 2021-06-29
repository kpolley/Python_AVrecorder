import threading
import queue
import time
import sys
import numpy
import sounddevice as sd
import soundfile as sf


class AudioRecorder:

    def __init__(self):

        self.open = True
        self.file_name = 'default_name'  # This will be replaced with the value given in self.start()
        self.channels = 1
        self.q = queue.Queue()

        # Get samplerate and set device
        device_info = sd.query_devices(0, 'input')
        self.samplerate = int(device_info['default_samplerate'])
        sd.default.device = 0

    def callback(self, indata, frames, time, status):

        # This is called (from a separate thread) for each audio block.
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def record(self):
        print("Starting audio recording")
        with sf.SoundFile(self.file_name, mode='x', samplerate=self.samplerate,
                          channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate,
                                channels=self.channels, callback=self.callback):

                while self.open:
                    file.write(self.q.get())

    def stop(self, rec_time):
        time.sleep(rec_time)
        self.open = False
        print("Finished audio recording")

    def start(self, file_name, file_dir):
        self.open = True
        self.file_name = '{}/{}.wav'.format(file_dir, file_name)

        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
