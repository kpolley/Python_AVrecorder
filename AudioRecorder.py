import threading
import queue
import sounddevice as sd
import soundfile as sf
import numpy

class AudioRecorder():

    def __init__(self, timestamp):

        self.open = True
        # Get samplerate
        device_info = sd.query_devices(2, 'input')
        self.samplerate = int(device_info['default_samplerate'])
        self.channels = 1
        self.audio_filename = '{}.wav'.format(timestamp)
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def record(self):
        print("starting stream...")
        with sf.SoundFile(self.audio_filename, mode='x', samplerate=self.samplerate,
                      channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate,
                                channels=self.channels, callback=self.callback):

                while(self.open == True):
                    file.write(self.q.get())

    def stop(self):
        print("stopping stream...")
        self.open = False

    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()