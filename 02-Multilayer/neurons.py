import numpy as np
import random
from enum import Enum


""" Sign function which can be translated by given value. Used as
    activation function for perceptron.

    - Parameters:
        - translation: breaking point for the function.

    - Usage:
        - Sign()(0.5)
            - returns sign function for unipolar sigmoidal function
"""
class Sign:
    def __call__(self, translation):
        def sign(x):
            if x < translation:
                return 0
            else:
                return 1
        return sign

    def derivative(self):
        def signDeriv(x):
            return 1
        return signDeriv


""" Sigmoidal function & its derivative for given beta. Used as
    Activation function for perceptron.

    - Parameters:
        - beta: sigmoidal function parameter. Its value affects
        function shape. The greater the value the steeper is the function.

    - Usage:
        - Sigm()(0.5)
            - returns: sigm(x) function with beta=0.5
        - Sigm().derivative(0.5)
            - returns sigmDeriv function
            with beta=0.5
"""
class Sigm:
    def __call__(self, beta):
        def sigm(x):
            return 1.0 / (1.0 + np.exp(-beta * x))
        sigm.__name__ += '({0:.3f})'.format(beta)
        return sigm

    def derivative(self, beta):
        def sigmDeriv(x):
            return beta * np.exp(-beta * x) / ((1.0 + np.exp(-beta * x))**2)
        sigmDeriv.__name__ += '({0:.3f})'.format(beta)
        return sigmDeriv


class Neuron:
    """ This is template class for both perceptron and sigmoidal neuron. Perceptron is able
    to specify which class object belongs to, returning only 0 or 1, whereas sigmoidal neuron can return
    every value from 0 to 1. """

    def __init__(self, weights, iid, activFunc, activFuncDeriv, lRate=0.05, bias=random.uniform(-1, 1)):
        self.__dict__['_weights'] = np.array(weights)
        self.__dict__['_activFunc'] = activFunc
        self.__dict__['_activFuncDeriv'] = activFuncDeriv
        self.__dict__['_bias'] = bias
        self.__dict__['_lRate'] = lRate
        self.__dict__['_inputValues'] = None
        self.__dict__['_error'] = None
        self.__dict__['_sum'] = None
        self.__dict__['_val'] = None
        self.__dict__['_iid'] = iid
        self.__dict__['_delta'] = []

    def process(self, inputs):
        self._inputValues = inputs
        self._sum = np.dot(np.array(self._inputValues), self._weights) + self._bias

        """ Process output """
        self._val = self._activFunc(self._sum)
        return self._val

    def train(self):
        for i in range(len(self._weights)):
            self._weights[i] += self._lRate * self._activFuncDeriv(self._sum) * self._inputValues[i] * self._delta

        self._bias = self._lRate * self._activFuncDeriv(self._sum) * self._delta

    def calculateDelta(self, childNeurons):
        """ Child neurons weights & deltas: """
        cWeights = []
        cDeltas = []
        for cnn in childNeurons:
            cWeights.append(cnn._weights[self._iid])
            cDeltas.append(cnn._delta)

        self._delta = np.dot(np.array(cWeights), np.array(cDeltas))

    """ Access method """
    def __getitem__(self, index):
        if index == 'val':
            return self._val
        elif index == 'sum':
            return self._sum
        elif index == 'error':
            return self._error
        elif index == 'delta':
            return self._delta


class Layer:
    def __init__(self, numOfNeurons, iid, numOfInputs, activFunc, activFuncDeriv):
        self.__dict__['_neurons'] = []
        self.__dict__['_numOfNeurons'] = numOfNeurons
        self.__dict__['_activFunc'] = activFunc
        self.__dict__['_activFuncDeriv'] = activFuncDeriv
        self.__dict__['_numOfInputs'] = numOfInputs
        self.__dict__['_iid'] = iid

        for i in range(numOfNeurons):
            w = [random.uniform(-1, 1) for _ in range(numOfInputs)]
            self._neurons.append(Neuron(w, i, activFunc, activFuncDeriv))

    def processNeurons(self, inputs):
        nnOutputs = []
        for nn in self._neurons:
            nnOutputs.append(nn.process(inputs))
        return nnOutputs

    def trainNeurons(self):
        outs = []
        for index, n in enumerate(self._neurons):
            n.train()
            outs.append(n._val)
        return outs

    def calculateDeltas(self, childLayer):
        for nn in self._neurons:
            nn.calculateDelta(childLayer._neurons)

    """ Access method """
    def __getitem__(self, index):
        if index == 'iid':
            return self._iid


class Multilayer:
    def __init__(self, numOfLayers, numOfNeurons, numOfInputs, activFuncs, activFuncDerivs):
        self.__dict__['_layers'] = []
        self.__dict__['_numOfLayers'] = numOfLayers
        self.__dict__['_numOfInputs'] = numOfInputs
        self.__dict__['_activFuncs'] = activFuncs
        self.__dict__['_activFuncDerivs'] = activFuncDerivs

        for i in range(numOfLayers):
            self._layers.append(
                Layer(numOfNeurons[i], i, numOfInputs[i], activFuncs[i], activFuncDerivs[i]
            ))

    def processLayers(self, inputs):
        lrOutputs = []

        for index,  lr in enumerate(self._layers):
            if index == 0:  # for the first layer
                lrOutputs.append(lr.processNeurons(
                    inputs
                ))
            else:   # for the rest of layers
                lrOutputs.append(lr.processNeurons(
                    lrOutputs[index-1]
                ))
        return lrOutputs[self._numOfLayers-1][0]

    def trainLayers(self, inputVector):
        lrOutputs = []
        """ Passing letter input through the entire net """
        for index,  lr in enumerate(self._layers):
            if index == 0:  # for the first layer
                lrOutputs.append(lr.processNeurons(
                    inputVector._x
                ))
            else:   # for the rest of layers
                lrOutputs.append(lr.processNeurons(
                    lrOutputs[index-1]
                ))

        """ BACKPROPAGATION:
                - Calculating delta for every neuron """
        finalDelta = inputVector._d - lrOutputs[self._numOfLayers-1][0]

        for index, lr in enumerate(reversed(self._layers)):
            if index == 0:  # for the last layer
                lr._neurons[0]._delta = finalDelta
            else:   # for the rest of layers
                lr.calculateDeltas(self._layers[len(self._layers)-index])

        """     - Weights adjusting """
        prevOuts = None
        for i in range(self._numOfLayers):
            prevOuts = self._layers[i].trainNeurons()

        return prevOuts

    """ Access method """
    def __getitem__(self, index):
        if index == 'layers':
            return self._layers
        elif index == 'numOfLayers':
            return self._numOfLayers