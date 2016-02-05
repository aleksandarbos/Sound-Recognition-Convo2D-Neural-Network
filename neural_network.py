import numpy as np
import cv2
import collections

# keras
from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD


class NeuralNetwork:

    def __init__(self):
        self.a = []

    @staticmethod
    def create_ann():
        ann = Sequential()
        ann.add(Dense(9625, input_dim=57750, activation='sigmoid')) # 165x350 je croppovana slika = 165*350=57750, skriveni sloj 128neurona
        ann.add(Dense(3, activation='sigmoid')) # izlazni sloj od 3 neurona
        return ann

    @staticmethod
    def train_ann(ann, X_train, y_train):
        X_train = np.array(X_train, np.float32)
        y_train = np.array(y_train, np.float32)

        # definisanje parametra algoritma za obucavanje
        sgd = SGD(lr=0.01, momentum=0.9)
        ann.compile(loss='mean_squared_error', optimizer=sgd)

        # obucavanje neuronske mreze
        ann.fit(X_train, y_train, nb_epoch=500, batch_size=1, verbose = 0, shuffle=False, show_accuracy = False)

        return ann

    @staticmethod
    def convert_output(outputs):
        return np.eye(len(outputs))

    @staticmethod
    def matrix_to_vector(image):
        return image.flatten()

    @staticmethod
    def scale_to_range(image):
        return image / 255

    @staticmethod
    def prepare_for_ann(bin_graphs):
        ready_for_ann = []
        for bin_graph in bin_graphs:
            ready_for_ann.append(NeuralNetwork.matrix_to_vector(NeuralNetwork.scale_to_range(bin_graphs)))
        return ready_for_ann

    @staticmethod
    def create_and_train_nn(bin_graphs):     # bin_graphs - ulazni niz grafika, kao numpy matrice
        alphabet = ['ASC','FLAT','DESC']     # uzlazni, ravan, opadajuci signal
        inputs = NeuralNetwork.prepare_for_ann(bin_graphs)
        outputs = NeuralNetwork.convert_output(alphabet)
        ann = NeuralNetwork.create_ann()
        ann = NeuralNetwork.train_ann(ann, inputs, outputs)


