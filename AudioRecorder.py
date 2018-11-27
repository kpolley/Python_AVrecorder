import threading
import queue
import numpy
import sounddevice as sd
import soundfile as sf

class AudioRecorder():

    def __init__(self):

        self.open = True
        self.file_name = 'default_name'
        self.channels = 1
        self.q = queue.Queue()
        
        # Get samplerate
        device_info = sd.query_devices(2, 'input')
        self.samplerate = int(device_info['default_samplerate'])

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

    def start(self, file_name, file_dir):
        self.open = True
        self.file_name = '{}/{}.wav'.format(file_dir, file_name)

        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()