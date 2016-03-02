import numpy as np
import cv2
import collections

from numpy.core.multiarray import ndarray

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
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D

from _tkinter import *

class NeuralNetwork:

    ann = None
    alphabet = ['ASC', 'DESC', 'FLAT', 'SOY']

    
    @staticmethod
    def create_convo2D_ann():
        NeuralNetwork.ann = Sequential()

        # input image dimensions
        img_rows, img_cols = 33, 70
        # number of convolutional filters to use
        nb_filters = 32
        # size of pooling area for max pooling
        nb_pool = 2
        # convolution kernel size
        nb_conv = 3

        NeuralNetwork.ann.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='valid', input_shape=(1, img_rows, img_cols)))
        NeuralNetwork.ann.add(Activation('sigmoid'))
        NeuralNetwork.ann.add(Convolution2D(nb_filters, nb_conv, nb_conv))
        NeuralNetwork.ann.add(Activation('sigmoid'))
        NeuralNetwork.ann.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
        NeuralNetwork.ann.add(Dropout(0.25))
        
        NeuralNetwork.ann.add(Flatten())
        NeuralNetwork.ann.add(Dense(128))
        NeuralNetwork.ann.add(Activation('sigmoid'))
        NeuralNetwork.ann.add(Dropout(0.5))
        NeuralNetwork.ann.add(Dense(4)) # 4 classes
        NeuralNetwork.ann.add(Activation('softmax'))

        NeuralNetwork.ann.compile(loss='categorical_crossentropy', optimizer='adadelta')

        return NeuralNetwork.ann    

    @staticmethod
    def train_convo2D_ann(ann, X_train, y_train):
        NeuralNetwork.ann.fit(X_train, y_train, batch_size=1, nb_epoch=20, show_accuracy=True, verbose=1)

    @staticmethod
    def create_and_train_convo2D_ann():
        NeuralNetwork.ann = NeuralNetwork.create_convo2D_ann()

        #loading graphs from hdd
        asc_img_samples, desc_img_samples, flat_img_samples, soy_img_samples = spectogram.load_data_set_graphs()

        X_train = np.concatenate((asc_img_samples, desc_img_samples, flat_img_samples, soy_img_samples), axis=0)
        X_train = X_train.reshape(X_train.shape[0], 1, 33, 70) # 33 num of rows, 70 num of columns
        X_train = X_train.astype('float32')

        #preparing outputs
        y11 = 0 * np.ones((1, len(asc_img_samples)))    #ASC
        y22 = 1 * np.ones((1, len(desc_img_samples)))   #DESC
        y33 = 2 * np.ones((1, len(flat_img_samples)))   #FLAT
        y44 = 3 * np.ones((1, len(soy_img_samples)))    #SOY

        y_train = np.concatenate((y11, y22, y33, y44), axis=1)
        y_train = y_train[0]  # switch to 1-dim array
        y_train = y_train.astype('float32')
        y_train = np_utils.to_categorical(y_train, 4) # 0000, 0010, 0100, 1000 for each class

        NeuralNetwork.train_convo2D_ann(NeuralNetwork.ann, X_train, y_train)
        NeuralNetwork.ann.save_weights('my_convo2d_model_weights.h5', overwrite=True)

    @staticmethod
    def create_and_train_nn():     # bin_graphs - ulazni niz grafika, kao numpy matrice
        NeuralNetwork.ann = NeuralNetwork.create_and_train_convo2D_ann()

    @staticmethod
    def predict_results():
        # generating graph
        spectogram.plotstft('test.wav', generatefig=True) # display user recorded sound and save plot
        test_img = cv2.imread('test.png', 0)    # load grayscale pic
        cv2.imshow('test.png', test_img) # display new pic

        X_test = []     # preparing input
        X_test.append(test_img)
        X_test = np.array(X_test)
        X_test = X_test.reshape(X_test.shape[0], 1, 33, 70) # 33 num of rows, 70 num of columns

        # testing input
        results_test = NeuralNetwork.ann.predict_classes(X_test, batch_size=1)
        result_probability = NeuralNetwork.ann.predict_proba(X_test, batch_size=1)
        result_probability *= 100   # convert to percent

        print "[Winner]: " + NeuralNetwork.alphabet[results_test]
        print "[Probabilities:] " + "ASC:" + str(result_probability[0, 0])+"%" + ", DESC:" + str(result_probability[0, 1])+"%" + \
                ", FLAT:" + str(result_probability[0, 2])+"%" + ", SOY: " + str(result_probability[0, 3])+"%"

    @staticmethod
    def load_model_weights():
       print "Creating neural network..."
       NeuralNetwork.create_convo2D_ann()
       print "Compiling neural network..."
       NeuralNetwork.ann.compile(loss='categorical_crossentropy', optimizer='adadelta')
       print "Loading neural network model weights..."
       NeuralNetwork.ann.load_weights('my_convo2d_model_weights.h5')
       print "Neural network successfully loaded!"
