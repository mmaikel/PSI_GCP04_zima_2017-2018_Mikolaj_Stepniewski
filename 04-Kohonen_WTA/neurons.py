# @Author: Mikołaj Stępniewski <maikelSoFly>
# @Date:   2017-12-12T17:15:51+01:00
# @Email:  mikolaj.stepniewski1@gmail.com
# @Filename: neurons.py
# @Last modified by:   maikelSoFly
# @Last modified time: 2017-12-16T23:31:39+01:00
# @License: Apache License  Version 2.0, January 2004
# @Copyright: Copyright © 2017 Mikołaj Stępniewski. All rights reserved.



import sys
# Add the include folder path to the sys.path list
sys.path.append('../include')
from neuron import *
from supportFunctions import *
from collections import Counter


class KohonenNeuron(Neuron):
    def __init__(self, numOfInputs, processFunc, iid, lRate=0.1):
        Neuron.__init__(self, numOfInputs, iid, activFunc=None, lRate=lRate, bias=0)
        self.__dict__['_winnerCounter'] = 0
        self.__dict__['_processFunc'] = processFunc
        self.__dict__['_startWeights'] = self._weights[:]
        self.__dict__['_errorHist'] = []

    def process(self, vector):
        self._error = self._processFunc(vector, self._weights)
        return self._error

    def train(self, vector):
        for i in range(len(self._weights)):
            self._weights[i] += self._lRate * (vector[i] - self._weights[i])

    def resetWeights(self):
        self._weights = self._startWeights[:]


""" Simple WTA for now...

    Winner is neuron with least distance
    between weights vector and input vector """
class KohonenNeuronGroup:
    def __init__(self, numOfInputs, numOfNeurons, processFunc, lRateFunc, lRate=0.1):
        self.__dict__['_numOfNeurons'] = numOfNeurons
        self.__dict__['_lRate'] = lRate
        self.__dict__['_numOfInputs'] = numOfInputs
        self.__dict__['_neurons'] = None
        self.__dict__['_processFunc'] = processFunc
        self.__dict__['_lRateFunc'] = lRateFunc
        self.__dict__['_currentLRate'] = None

        self._neurons = [[KohonenNeuron(numOfInputs, processFunc, iid=i*numOfNeurons[0]+j, lRate=lRate)
            for i in range(numOfNeurons[0])]
            for j in range(numOfNeurons[1])
        ]


    def resetWeights(self):
        for row in self._neurons:
            for neuron in row:
                neuron.resetWeights()

    def resetWins(self):
        for row in self._neurons:
            for neuron in row:
                neuron._winnerCounter = 0

    def setLRate(self, lRate):
        self._currentLRate = lRate
        for row in self._neurons:
            for neuron in row:
                neuron._lRate = lRate


    def train(self, vectors, histFreq=1, retMostCommon=False):
        winners = []
        for i, vector in enumerate(vectors):
            winner = None
            for row in self._neurons:
                for neuron in row:
                    neuron.process(vector)
                    if winner == None:
                        winner = neuron
                    elif winner != None:
                        if neuron._error < winner._error:
                            winner = neuron

            """ Winner Takes All """
            if winner._winnerCounter % histFreq == 0:
                winner._errorHist.append(winner._error)
            winner._winnerCounter += 1
            winner.train(vector)
            winners.append(winner)

        self.setLRate(self._lRateFunc(self._lRate))

        if retMostCommon:
            return Counter(winners).most_common(1)[0][0]

        return winners


    """ Basicaly the same as above, but without updating weights """
    def classify(self, vectors):
        winners = []
        for i, vector in enumerate(vectors):
            winner = None
            for row in self._neurons:
                for neuron in row:
                    neuron.process(vector)
                    if winner == None:
                        winner = neuron
                    elif winner != None:
                        if neuron._error < winner._error:
                            winner = neuron

            winners.append(winner)

        return winners


    """ Access methods """
    def __getitem__(self, key):
        if key == 'totalNumOfNeurons':
            return sum(len(x) for x in self._neurons)
