#!/usr/bin/env python
#coding: utf-8
""" This work is licensed under a Creative Commons Attribution 3.0 Unported License.
    Frank Zalkow, 2012-2013 """
from PIL import Image
import numpy as np
import scipy.io.wavfile as wav
import cv2
import os

from matplotlib import pyplot as plt
from numpy.lib import stride_tricks
from image_transform import ImageTransform
from scipy.spatial import distance



""" short time fourier transform of audio signal """
def stft(sig, frameSize, overlapFac=0.5, window=np.hanning):
    win = window(frameSize)
    hopSize = int(frameSize - np.floor(overlapFac * frameSize))

    # zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(np.floor(frameSize/2.0)), sig)
    # cols for windowing
    cols = np.ceil( (len(samples) - frameSize) / float(hopSize)) + 1
    # zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frameSize))

    frames = stride_tricks.as_strided(samples, shape=(cols, frameSize), strides=(samples.strides[0]*hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)

""" scale frequency axis logarithmically """
def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))

    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,scale[i]:], axis=1)
        else:
            newspec[:,i] = np.sum(spec[:,scale[i]:scale[i+1]], axis=1)

    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i+1]])]

    return newspec, freqs

""" plot spectrogram"""
def plotstft(audiopath, binsize=2**10, plotpath=None, colormap="jet"): #colormap="jet"
    samplerate, samples = wav.read(audiopath)
    s = stft(samples, binsize)

    sshow, freq = logscale_spec(s, factor=18.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    fig = plt.figure(figsize=(8, 4.25))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("Time [s]")
    plt.ylabel("Frequency dB[Hz]")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 20)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    #if plotpath:
    #    plt.savefig(plotpath, bbox_inches="tight")
    #else:
    #    plt.show()

    #plt.clf()

    fig.canvas.draw()       # bitno!!! formira model grafika tj samu matricu grafika, ali je ne prikazuje korisniku!
    plt.show()
    """ -temp- deo samo za prikaz sta ce ici u obucavanje mreze... posle obrisati.. """
    # odlicno radi...
    img_data = ImageTransform.fig2data(fig)
    img_data = ImageTransform.transform(img_data)
    plt.imshow(img_data, 'gray')
    plt.figure()
    img_data = ImageTransform.image_bin(img_data)
    img_data = ImageTransform.invert(img_data)
    img_data = ImageTransform.remove_noise(img_data) # zatvaranje 1.dilate 2.erode
    img_data = ImageTransform.resize_graph(img_data, 70, 33) #org 350x165, 350%5=70, 165%5=33, odrzane proporcije
    cv2.imwrite("test.png", img_data)
    plt.imshow(img_data, 'gray')
    plt.show()

    #img_data = prepare_fig_to_img(fig)      za formiranje grafika u data-set-u ... TODO: napraviti zasebnu fun..
    #cv2.imwrite(plotpath, img_data)

    return fig      # vrati matlabov plot obj(numpy array)

def read_data_set():
    """
    @brief
    Funkcija koja ucitava sa standardnih direktorijuma data seta samples/ ASC,DESC,FLAT
    ucitane .wav datoteke pretvara u matlab fig grafik objekte
    Izlaz: liste ASC, DESC, FLAT matlab fig grafik objekata respektivno.
    """

    asc_fig_graphs = []
    desc_fig_graphs = []
    flat_fig_graphs = []

    for asc_file in os.listdir("samples/ASC"):
        if asc_file.endswith(".wav"):
            asc_fig_graphs.append(plotstft("samples/ASC/" + asc_file))    # dodaj u ucitane matlabove fig objete

    for desc_file in os.listdir("samples/DESC"):
        if desc_file.endswith(".wav"):
            desc_fig_graphs.append(plotstft("samples/DESC/" + desc_file))    # dodaj u ucitane matlabove fig objete

    for flat_file in os.listdir("samples/FLAT"):
        if flat_file.endswith(".wav"):
            flat_fig_graphs.append(plotstft("samples/FLAT/" + flat_file))    # dodaj u ucitane matlabove fig objete

    return asc_fig_graphs, desc_fig_graphs, flat_fig_graphs



def prepare_fig_to_img(graph_fig):
    """
    @brief
    Ulaz: matlabov grafik objekat
    Matlabova figura postaje slika, nad slikom se vrsi
    1. crop-ovanje
    2. grayscale
    3. binarizacija
    4. uklanjanje suma
    5. resize
    Izlaz: slika spremna za obucavanje mreze
    """
    img_data = ImageTransform.fig2data(graph_fig)
    img_data = ImageTransform.transform(img_data)
    img_data = ImageTransform.image_bin(img_data)
    img_data = ImageTransform.invert(img_data)
    img_data = ImageTransform.remove_noise(img_data) # zatvaranje 1.dilate 2.erode
    img_data = ImageTransform.resize_graph(img_data, 70, 33) #org 350x165, 350%5=70, 165%5=33, odrzane proporcije
    return img_data

def figs_to_img_prepare(asc_graphs_fig, desc_graphs_fig, flat_graphs_fig):
    """
    @brief
    Ulaz: matlab grafici iz ASC, DESC, FLAT foldera, respektivno.
    Funkcija koja matlabove fig objekte pretvara u numpy matrice- tj. img objekte
    vrsi transformacije nad slikama i sprema ih za ulazni obucavajuci sloj n. mreze.
    Izlaz: matrica 3xn koja se sadrzi od 3 kolone za svaki od tipova grafika.
    """

    asc_array = []
    desc_array = []
    flat_array = []

    learning_array = []

    for asc_fig in asc_graphs_fig:
        asc_img = prepare_fig_to_img(asc_fig)
        asc_array.append(asc_img)

    for desc_fig in desc_graphs_fig:
        desc_img = prepare_fig_to_img(desc_fig)
        desc_array.append(desc_img)

    for flat_fig in flat_graphs_fig:
        flat_img = prepare_fig_to_img(flat_fig)
        flat_array.append(flat_img)

    learning_array[0]=asc_array;
    learning_array[1]=desc_array;
    learning_array[2]=flat_array;

    return learning_array

