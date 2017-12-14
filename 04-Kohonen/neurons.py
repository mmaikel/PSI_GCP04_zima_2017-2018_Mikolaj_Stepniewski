import sys
# Add the neuron folder path to the sys.path list
sys.path.append('../inc')
from neuron import *


class KohonenNeuron(Neuron):
    def __init__(self, numOfInputs, processFunc, iid, lRate=0.1):
        Neuron.__init__(self, numOfInputs, iid, activFunc=None, lRate=lRate, bias=0)
        self.__dict__['_winnerCounter'] = 0
        self.__dict__['_pausedCounter'] = 0
        self.__dict__['_processFunc'] = processFunc
        self.__dict__['_startWeights'] = self._weights[:]

    def process(self, vector):
        self._sum = self._processFunc(vector, self._weights)
        return self._sum

    def train(self, vector):
        for i in range(len(self._weights)):
            self._weights[i] += self._lRate * (vector[i] - self._weights[i])

    def resetWeights(self):
        self._weights = self._startWeights[:]


""" Simple WTA for now...

    Winner is neuron with least distance
    between weights vector and input vector """
class KohonenNeuronGroup:
    def __init__(self, numOfInputs, numOfNeurons, processFunc, trainingData, lRateFunc, lRate=0.1):
        self.__dict__['_numOfNeurons'] = numOfNeurons
        self.__dict__['_lRate'] = lRate
        self.__dict__['_numOfInputs'] = numOfInputs
        self.__dict__['_neurons'] = []
        self.__dict__['_trainingData'] = trainingData
        self.__dict__['_processFunc'] = processFunc
        self.__dict__['_lRateFunc'] = lRateFunc
        self.__dict__['_currentLRate'] = None

        for i in range(numOfNeurons):
            neuron = KohonenNeuron(numOfInputs, processFunc, i, lRate)
            neuron.setTrainingData(trainingData)
            self._neurons.append(neuron)

    def resetWeights(self):
        for neuron in self._neurons:
            neuron.resetWeights()

    def resetWins(self):
        for neuron in self._neurons:
            neuron._winnerCounter = 0


    def train(self, vectors):
        winner = None
        for i, vector in enumerate(vectors):
            if i % 50 == 0:
                print(i, "^^^^^")

            winner = None
            for neuron in self._neurons:
                neuron.process(vector)
                if winner == None:
                    winner = neuron
                elif winner != None:
                    if neuron._sum < winner._sum:
                        winner = neuron

                winner._winnerCounter += 1
            print(winner._iid)


        self._currentLRate = self._lRate * self._lRateFunc()

        return winner
