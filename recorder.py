from datetime import datetime
import pyaudio
import wave

class Recorder:

    global filename

    @staticmethod
    def start_recording():
        CHUNK = 1024
        FORMAT = pyaudio.paInt16 #paInt8
        CHANNELS = 1
        RATE = 44100 #sample rate 44100
        RECORD_SECONDS = 3
        #WAVE_OUTPUT_FILENAME = "sound_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"
        WAVE_OUTPUT_FILENAME = "test.wav"
        filename = WAVE_OUTPUT_FILENAME

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK) #buffer

        print("* recording")

        frames = []

        end_value = int(RATE / CHUNK * RECORD_SECONDS) + 1
        print end_value
        for i in range(0, end_value):
            data = stream.read(CHUNK)
            frames.append(data) # 2 bytes(16 bits) per channel

        print("* done recording")

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()