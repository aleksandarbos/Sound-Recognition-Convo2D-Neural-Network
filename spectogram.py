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
def plotstft(audiopath, generatefig=True, binsize=2**10, plotpath=None, colormap="jet"): #colormap="jet"
    samplerate, samples = wav.read(audiopath)
    s = stft(samples, binsize)

    audio_path_split = audiopath.split('/')
    if len(audio_path_split)-1 > 0:
        plotpath = audio_path_split[0] + "/" + audio_path_split[1] + "/graphs/" + audio_path_split[2] # dodaj folder graphs u putanju za cuvanje grafika
        plotpath = plotpath.replace('.wav', '.png')            # zameni ekstenziju fajla na .png

    plotpath = audiopath.replace('.wav', '.png')

    sshow, freq = logscale_spec(s, factor=80.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    fig = plt.figure(figsize=(8, 4.25))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("Time [s]")
    plt.ylabel("Frequency dB[Hz]")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 10))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 20)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])

    #plt.clf()

    fig.canvas.draw()       # bitno!!! formira model grafika tj samu matricu grafika, ali je ne prikazuje korisniku!

    if not(generatefig):
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
    else:
        img_data = prepare_fig_to_img(fig)      #za formiranje grafika u data-set-u ... TODO: napraviti zasebnu fun..
        cv2.imwrite(plotpath, img_data)


    return fig      # vrati matlabov plot obj(numpy array)

def create_data_set_graphs():
    """
    @brief
    Funkcija koja ucitava sa standardnih direktorijuma data seta samples/ ASC,DESC,FLAT
    ucitane .wav datoteke pretvara u png grafike koji se nalaze u samples/graphs/ ASC,DESC,FLAT
    """

    for asc_file in os.listdir("samples/ASC"):
        if asc_file.endswith(".wav"):
            fig = plotstft("samples/ASC/" + asc_file, generatefig=True)
            asc_file = asc_file.replace('.wav', '.png')
            img_data = prepare_fig_to_img(fig)      #za formiranje grafika u data-set-u ...
            cv2.imwrite("samples/ASC/graphs/" + asc_file, img_data)

    for desc_file in os.listdir("samples/DESC"):
        if desc_file.endswith(".wav"):
            fig = plotstft("samples/DESC/" + desc_file, generatefig=True)
            desc_file = desc_file.replace('.wav', '.png')
            img_data = prepare_fig_to_img(fig)      #za formiranje grafika u data-set-u ...
            cv2.imwrite("samples/DESC/graphs/" + desc_file, img_data)

    for flat_file in os.listdir("samples/FLAT"):
        if flat_file.endswith(".wav"):
            fig = plotstft("samples/FLAT/" + flat_file, generatefig=True)
            flat_file = flat_file.replace('.wav', '.png')
            img_data = prepare_fig_to_img(fig)      #za formiranje grafika u data-set-u ...
            cv2.imwrite("samples/FLAT/graphs/" + flat_file, img_data)

    for soy_file in os.listdir("samples/SOY"):
        if soy_file.endswith(".wav"):
            fig = plotstft("samples/SOY/" + soy_file, generatefig=True)
            soy_file = soy_file.replace('.wav', '.png')
            img_data = prepare_fig_to_img(fig)      #za formiranje grafika u data-set-u ...
            cv2.imwrite("samples/SOY/graphs/" + soy_file, img_data)




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
    Izlaz: slika spremna za obucavanje mreze (numpy matrica)
    """
    img_data = ImageTransform.fig2data(graph_fig)
    img_data = ImageTransform.transform(img_data)
    img_data = ImageTransform.image_bin(img_data)
    img_data = ImageTransform.invert(img_data)
    img_data = ImageTransform.remove_noise(img_data) # zatvaranje 1.dilate 2.erode
    img_data = ImageTransform.resize_graph(img_data, 70, 33) #org 350x165, 350%5=70, 165%5=33, odrzane proporcije
    return img_data

def load_data_set_graphs():
    """
    @brief
    Funkcija koja ucitava sa standardnih direktorijuma data seta samples/graphs/ ASC,DESC,FLAT
    ucitane .png datoteke pretvara numpy matrice spremne za dalji rad
    Izlaz: 4 matrice: ASC 1xn matrica img objekta , DESC 1xn matrica img objekta , FLAT 1xn matrica img objekta, SOY 1xn matrica img objekta
    """

    asc_graphs_array = []
    desc_graphs_array = []
    flat_graphs_array = []
    soy_graphs_array = []

    for asc_file in os.listdir("samples/ASC/graphs/"):
        if asc_file.endswith(".png"):
            img_data = cv2.imread("samples/ASC/graphs/" + asc_file)
            asc_graphs_array.append(img_data)

    for desc_file in os.listdir("samples/DESC/graphs/"):
        if desc_file.endswith(".png"):
            img_data = cv2.imread("samples/DESC/graphs/" + desc_file)
            desc_graphs_array.append(img_data)

    for flat_file in os.listdir("samples/FLAT/graphs/"):
        if flat_file.endswith(".png"):
            img_data = cv2.imread("samples/FLAT/graphs/" + flat_file)
            flat_graphs_array.append(img_data)

    for soy_file in os.listdir("samples/SOY/graphs/"):
        if soy_file.endswith(".png"):
            img_data = cv2.imread("samples/SOY/graphs/" + soy_file)
            soy_graphs_array.append(img_data)


    return asc_graphs_array, desc_graphs_array, flat_graphs_array, soy_graphs_array