import numpy as np
import cv2
import collections
import spectogram
import json
import gui

# keras
from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import model_from_json

from _tkinter import *

class NeuralNetwork:

    ann = None
    alphabet = ['ASC', 'DESC', 'FLAT', 'SOY']

    @staticmethod
    def create_ann():
        NeuralNetwork.ann = Sequential()
        NeuralNetwork.ann.add(Dense(770, input_dim=2310, activation='sigmoid')) # 70x33 je croppovana slika = 70*33=, skriveni sloj 128neurona
        NeuralNetwork.ann.add(Dense(4, activation='sigmoid')) # izlazni sloj od 4 neurona
        return NeuralNetwork.ann

    @staticmethod
    def train_ann(ann, X_train, y_train):
        X_train = np.array(X_train, np.float32)
        y_train = np.array(y_train, np.float32)

        # definisanje parametra algoritma za obucavanje
        sgd = SGD(lr=0.01, momentum=0.9)
        ann.compile(loss='mean_squared_error', optimizer=sgd)

        # obucavanje neuronske mreze
        ann.fit(X_train, y_train, nb_epoch=20, batch_size=1, verbose = 1, shuffle=True, show_accuracy = True)

        return ann

    @staticmethod
    def prepare_for_ann(bin_graphs, batch=True): # batch govori da li vise grafika spremam za mrezu ili samo 1 (vise za training, 1 za predict)
        ready_for_ann = []
        if batch:
            for bin_graph in bin_graphs:# deo primeme za training
                bb = bin_graph[:,:,0]
                bb = bb.flatten()
                bb /= 255
                ready_for_ann.append(bb)
        else:                           # deo pripreme za predict...
            bb = bin_graphs[:,:,0]
            bb = bb.flatten()
            bb /= 255
            ready_for_ann.append(bb)
        return np.array(ready_for_ann)

    @staticmethod
    def create_and_train_nn():     # bin_graphs - ulazni niz grafika, kao numpy matrice
        #alphabet = ['ASC','DESC','FLAT']     # uzlazni, opadajuci, ravan signal
        NeuralNetwork.ann = NeuralNetwork.create_ann()
        asc_img_samples, desc_img_samples, flat_img_samples, soy_img_samples = spectogram.load_data_set_graphs() # ucitavanje sa diska u numpy matrice (img objekte)

        X_train = np.concatenate((asc_img_samples, desc_img_samples, flat_img_samples, soy_img_samples), axis=0)
        y_train = np.array([0])

        X_train = X_train.astype('float32')
        X_train = NeuralNetwork.prepare_for_ann(X_train) # slozi u binarni oblik i vektorki oblik slike

        #objasni mrezi koja slika je koja onim redosledom koji je u X_train
        y1_seg = [] #asc
        y2_seg = [] #desc
        y3_seg = [] #flat
        y4_seg = [] #soy

        for i in range(0, len(asc_img_samples)):
            y1_seg.append(0) #ASC

        for i in range(0, len(desc_img_samples)):
            y2_seg.append(1) #DESC

        for i in range(0, len(flat_img_samples)):
            y3_seg.append(2) #FLAT

        for i in range(0, len(soy_img_samples)):
            y4_seg.append(3) #FLAT

        y_train = np.concatenate((y1_seg, y2_seg, y3_seg, y4_seg), axis=0)
        y_train = y_train.astype('float32')
        y_train = np_utils.to_categorical(y_train, 4) # broj kasa na koje se rastavlja je 4

        NeuralNetwork.ann = NeuralNetwork.train_ann(NeuralNetwork.ann, X_train, y_train)
        json_string = NeuralNetwork.ann.to_json()
        with open('model_weights.json', 'w') as outfile:
            json.dump(json_string, outfile)
        NeuralNetwork.ann.save_weights('my_model_weights.h5', overwrite=True)


    @staticmethod
    def winner(output): # output je vektor sa izlaza neuronske mreze
        return np.argmax(output)

    @staticmethod
    def display_result(outputs, alphabet):
        return alphabet[NeuralNetwork.winner(outputs)]

    @staticmethod
    def predict_results():
        spectogram.plotstft('test.wav', generatefig=True)
        test_img = cv2.imread('test.png')
        cv2.imshow('test.png', test_img)
        inputs_test = NeuralNetwork.prepare_for_ann(test_img, batch=False) # samo jednu sliku pripremam
        results_test = NeuralNetwork.ann.predict(np.array(inputs_test, np.float32))
        print "ASC: " + str(results_test[0,0]) + ", DESC: " + str(results_test[0,1]) + ", FLAT: " + str(results_test[0, 2]) + ", SOY: " + str(results_test[0, 3])
        print "[Winner]: " + NeuralNetwork.display_result(results_test, NeuralNetwork.alphabet)

    @staticmethod
    def load_model_weights():
       print "Creating neural network..."
       NeuralNetwork.create_ann()
       print "Compiling neural network..."
       sgd = SGD(lr=0.01, momentum=0.9)
       NeuralNetwork.ann.compile(loss='mean_squared_error', optimizer=sgd)
       print "Loading neural network model weights..."
       NeuralNetwork.ann.load_weights('my_model_weights.h5')
       print "Neural network successfully loaded!"
