import threading
import wave

import pyaudio


class AudioRecorder:

    def __init__(self):
        self.audio = pyaudio.pyAudio()  # create pyaudio instantiation
        self.open = True
        self.file_name = 'default_name'  # This will be replaced with the value given in self.start()
        self.form_1 = pyaudio.paInt16  # 16 bit resolution
        self.channels = 1  # 1 channel
        self.chunk = 4096  # 2612 samples for buffer
        self.dev_index = 0  # device index found by p.get_device_info_by_index(ii)
        self.samp_rate = 44100  # 44.1kHz sampling rate

    def record(self, rec_time):
        # create pyaudio stream
        stream = self.audio.open(format=self.form_1, rate=self.samp_rate, channels=self.channels,
                                 input_device_index=self.dev_index, input=True,
                                 frames_per_buffer=self.chunk)
        print("Starting audio recording")
        self.frames = []
        # loop through stream and append audio chunks to frame array
        for ii in range(0, int((self.samp_rate / self.chunk) * rec_time)):
            data = stream.read(self.chunk)
            self.frames.append(data)

        print("Finished audio recording")

        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        self.save_audio()

    def save_audio(self):
        wavefile = wave.open(self.file_name, 'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()

    def start(self, file_name, file_dir, rec_time):
        self.file_name = '{}/{}.wav'.format(file_dir, file_name)

        audio_thread = threading.Thread(target=self.record, args=rec_time)
        audio_thread.start()
