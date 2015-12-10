import sys
import wave
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
from scipy.fftpack import fft
from pylab import *

class Analyzer:
    @staticmethod
    def plot_sound():
        spf = wave.open('jest.wav','r')

        #Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')
        fs = spf.getframerate()

        #If Stereo
        if spf.getnchannels() == 2:
            print 'Just mono files'
            sys.exit(0)


        Time=np.linspace(0, len(signal)/fs, num=len(signal))

        plt.figure(1)
        plt.title('Signal Wave...')
        plt.plot(Time,signal)
        plt.show()

    @staticmethod
    def plot_frequency():
        fs, data = scipy.io.wavfile.read('jest.wav') # load the data
        a = data.T[0] # this is a two channel soundtrack, I get the first track
        b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
        c = fft(b) # create a list of complex number
        d = len(c)/2  # you only need half of the fft list
        plt.plot(abs(c[:(d-1)]),'r')
        plt.show()
        savefig('jest'+'.png',bbox_inches='tight')