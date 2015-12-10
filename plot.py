import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from scipy.fftpack import fft

def plot_audio(file_name, plot_type):
    spf = wave.open('samples/'+file_name,'r')

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')
    global fs
    fs = spf.getframerate()

    #If Stereo
    if spf.getnchannels() == 2:
        print 'Just mono files'
        sys.exit(0)

    if(plot_type == "raw"):
        plot_raw_audio(signal)
    elif(plot_type == "fft"):
        plot_fft_audio(signal)

def plot_raw_audio(signal):
    Time=np.linspace(0, len(signal)/fs, num=len(signal))
    plt.figure(1)
    plt.title('Raw Signal Wave...')
    plt.plot(Time,signal)
    plt.show()

def plot_fft_audio(signal):
    b=[(ele/2**8.)*2-1 for ele in signal] # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(b) # create a list of complex number
    d = len(c)/2  # you only need half of the fft list
    plt.title("FFT Signal Wave...")
    plt.plot(abs(c[:(d-1)]),'r')
    plt.show()
    #savefig(filename+'.png',bbox_inches='tight')
