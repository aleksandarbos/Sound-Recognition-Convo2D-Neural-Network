import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from scipy.fftpack import fft
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
from decimal import *

class Plot:

    sub_arrays = 6  # promenljiva koja daje broj podgrafika

    @staticmethod
    def plot_raw_audio(signal):
        dimensions=len(signal)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        verts = []
        zs = range(Plot.sub_arrays)

        for z in zs:
            ys = signal[z]
            ys[0] = 0           # kako bi pocetna i krajnja vrednost bile identicne..
            ys[len(ys)-1] = 0   # ..bitno utice da grafik izgleda normalno
            xs = np.linspace(0.0, 1.0, num=len(signal[z]))
            verts.append(list(zip(xs, ys)))

        poly = PolyCollection(verts, facecolors=[colorConverter.to_rgba('r', alpha=0.6)])
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlim3d(0, 1)
        ax.set_ylim3d(0, Plot.sub_arrays-1)
        ax.set_zlim3d(-50000, 50000)    # eventualno prilagoti raspon ose (zavisi od intenziteta zvuka koji je ucitan, i od broja podgrafika)

        plt.show()

    @staticmethod
    def plot_fft_audio(signal):
        dimensions=len(signal)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        verts = []
        zs = range(Plot.sub_arrays)

        for z in zs:
            b=[(ele/2**8.)*2-1 for ele in signal[z]] # this is 8-bit track, b is now normalized on [-1,1)
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
    def plot_audio(file_name, plot_type):
        spf = wave.open(file_name,'r')

        #Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, 'Int16')

        signal = np.array_split(signal, Plot.sub_arrays)

        global fs
        fs = spf.getframerate()

        #If Stereo
        if spf.getnchannels() == 2:
            print 'Just mono files'
            sys.exit(0)

        if(plot_type == "raw"):
            Plot.plot_raw_audio(signal)
        elif(plot_type == "fft"):
            Plot.plot_fft_audio(signal)

