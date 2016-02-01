from datetime import datetime
import pyaudio
import wave

class Recorder:

    @staticmethod
    def start_recording():
        #WAVE_OUTPUT_FILENAME = "sound_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        record_seconds = 5                  # duration of recording
        chunk = 1024
        channels = 1
        format = pyaudio.paInt16   # paInt8
        rate = 44100               # sample rate 44.1KHz
        file_output_name = "test.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk) #buffer

        print("* recording")

        frames = []

        end_value = int(rate / chunk * record_seconds) + 1
        print end_value
        for i in range(0, end_value):
            data = stream.read(chunk)
            frames.append(data) # 2 bytes(16 bits) per channel

        print("* done recording")

        wf = wave.open(file_output_name, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()