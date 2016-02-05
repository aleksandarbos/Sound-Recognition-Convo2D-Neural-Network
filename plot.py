import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from mpl_toolkits.mplot3d import Axes3D
from scipy.fftpack import fft
from scipy.interpolate import interp1d
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
from scipy import signal
from decimal import *
from spectogram import plotstft

from sympy.physics.quantum.matrixutils import scipy_sparse_matrix


class Plot:

    sub_arrays = 6  # promenljiva koja daje broj podgrafika


    @staticmethod
    def plot_raw_audio(opened_signal):
        dimensions=len(opened_signal)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        verts = []
        zs = range(Plot.sub_arrays)

        for z in zs:
            ys = opened_signal[z]
            ys[0] = 0           # kako bi pocetna i krajnja vrednost bile identicne..
            ys[len(ys)-1] = 0   # ..bitno utice da grafik izgleda normalno
            xs = np.linspace(0.0, 1.0, num=len(opened_signal[z]))
            verts.append(list(zip(xs, ys)))

        poly = PolyCollection(verts, facecolors=[colorConverter.to_rgba('r', alpha=0.6)])
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlim3d(0, 1)
        ax.set_ylim3d(0, Plot.sub_arrays-1)
        ax.set_zlim3d(-50000, 50000)    # eventualno prilagoti raspon ose (zavisi od intenziteta zvuka koji je ucitan, i od broja podgrafika)

        plt.show()

    @staticmethod
    def plot_fft_audio(opened_signal):
        dimensions=len(opened_signal)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        verts = []
        zs = range(Plot.sub_arrays)

        for z in zs:
            b=[(ele/2**8.)*2-1 for ele in opened_signal[z]] # this is 8-bit track, b is now normalized on [-1,1)
            c = fft(b) # create a list of complex number
            d = 5000
            c[0] = 0            # kako bi pocetna i krajnja vrednost bile identicne..
            c[len(b)-1] = 0     # ..bitno utice da grafik izgleda normalno
            ys = abs(c[:(d-1)])
            xs = np.linspace(0, d-1)
            verts.append(list(zip(xs, ys)))

        poly = PolyCollection(verts, facecolors=[colorConverter.to_rgba('r', alpha=0.6)])
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlim3d(0, 5000)
        ax.set_ylim3d(0, Plot.sub_arrays-1)
        ax.set_zlim3d(0, 8000000)       # eventualno prilagoti raspon ose (zavisi od intenziteta zvuka koji je ucitan, i od broja podgrafika)

        plt.show()
        #savefig(filename+'.png',bbox_inches='tight')

    @staticmethod
    def plot_audio(full_file_path, plot_type, radioIntVar):
        spf = wave.open(full_file_path,'r')

        #Extract Raw Audio from Wav File
        opened_signal = spf.readframes(-1)
        opened_signal = np.fromstring(opened_signal, 'Int16')

        #opened_signal = np.array_split(opened_signal, Plot.sub_arrays)

        global fs
        fs = spf.getframerate()

        #If Stereo
        if spf.getnchannels() == 2:
            print 'Just mono files'
            sys.exit(0)

        if(radioIntVar.get() == 1):   # is 2D plot
           if(plot_type == "raw"):
               Plot.plot_raw_audio2D(opened_signal)
           elif(plot_type == "fft"):
               Plot.plot_fft_audio2D(opened_signal)
           elif(plot_type == "spectrogram"):
               #Plot.plot_spectrogram2D(opened_signal)
                plotstft(full_file_path)
        elif(radioIntVar.get() == 2): #multi dimensional plot
           opened_signal = np.array_split(opened_signal, Plot.sub_arrays)
           if(plot_type == "raw"):
               Plot.plot_raw_audio(opened_signal)
           elif(plot_type == "fft"):
               Plot.plot_fft_audio(opened_signal)


    @staticmethod
    def plot_fft_audio2D(opened_signal):
        b=[(ele/2**8.)*2-1 for ele in opened_signal] # this is 8-bit track, b is now normalized on [-1,1)
        c = fft(b) # create a list of complex number
        #d = len(c)/2  # you only need half of the fft list
        d = 5000
        plt.title("2D FFT Signal Wave...")
        plt.plot(abs(c[:(d-1)]),'r')
        plt.show()
        #savefig(filename+'.png',bbox_inches='tight')


    @staticmethod
    def plot_raw_audio2D(opened_signal):
        Time=np.linspace(0, len(opened_signal)/fs, num=len(opened_signal))
        plt.figure(1)
        plt.title('2D Raw Signal Wave...')
        plt.plot(Time, opened_signal)
        plt.show()

    @staticmethod
    def plot_spectrogram2Dv2(opened_signal):
        # Compute and plot the spectrogram.
        f, t, Sxx = signal.spectrogram(opened_signal, 10e3)
        #print "len(t): " + str(len(t)) + ", len(f): " + str(len(f)) + ", len(Sxx): " + str(len(Sxx))
        #print "ln - first index: " + str(np.log(f[1])) + ", last index: " + str(np.log(f[len(f)-1]))

        # logf = interp1d(np.log(f[1]), np.log(f[len(f)]))
        f[0] = 50.0

        plt.pcolormesh(t, f, Sxx)
        plt.ylabel('ln(Frequency [Hz])')
        plt.xlabel('Time [sec]')
        plt.yscale('log')
        #plt.axis([0,3,0,0.25])
        plt.show()

    @staticmethod
    def plot_spectrogram2D(opened_signal):  # verzija 2
        # Compute and plot the spectrogram.
        plt.specgram(opened_signal) # pogledati jos sve parametre
        plt.show()

