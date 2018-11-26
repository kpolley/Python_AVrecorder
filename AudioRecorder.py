import threading
import queue
import sounddevice as sd
import soundfile as sf
import numpy

class AudioRecorder():

    def __init__(self):

        self.open = True
        self.file_name = None
        # Get samplerate
        device_info = sd.query_devices(2, 'input')
        self.samplerate = int(device_info['default_samplerate'])
        self.channels = 1
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def record(self):
        with sf.SoundFile(self.file_name, mode='x', samplerate=self.samplerate,
                      channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate,
                                channels=self.channels, callback=self.callback):

                while(self.open == True):
                    file.write(self.q.get())

    def stop(self):
        self.open = False

    def start(self, timestamp):
        self.file_name = '{}.wav'.format(timestamp)

        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()