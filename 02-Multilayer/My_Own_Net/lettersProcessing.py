from neurons import *
from letters import *
import numpy as np
import math
from prettytable import PrettyTable

""" Mean Squared Error function """
def MSE(results,expected):
    sum = 0.0
    for i in range(len(results)):
        sum+=(results[i]-expected[i])**2
    return sum/len(results)


class InputVector:
    def __init__(self, x, d):
        self.__dict__['_x'] = x
        self.__dict__['_d'] = d
    def __getitem__(self, index):
        if index == 'x':
            return self._x
        if index == 'd':
            return self._d


if __name__ == "__main__":

    ml = Multilayer(
        3,                                              # number of layers
        [35, 15, 1],                                    # number of neurons in layers
        [35, 35, 15],                                   # number of inputs in layers
        [Sigm()(1.0), Sigm()(1.0), Linear()()],         # activation functions in layers
        [
            Sigm().derivative(1.0),                     # activation function derivatives in layers
            Sigm().derivative(1.0),
            Linear().derivative(),
        ]
    )

    # TRAINING LETTERS
    lettersInput = [
        LetterInput('a'),
        LetterInput('p'),
        LetterInput('o'),
        LetterInput('b'),
        LetterInput('A'),
        LetterInput('B'),
        LetterInput('C'),
        LetterInput('I'),
        LetterInput('F'),
        LetterInput('d'),
        LetterInput('c'),
        LetterInput('w'),
        LetterInput('H'),
        LetterInput('D')
    ]

    print("Epoch", ",", "MSE error")
    aboveErr = True
    expectedForAllLetters = []
    for j in range(len(lettersInput)):
        expectedForAllLetters.append(ord(lettersInput[j]._letter))
    epoch = 0
    results = []
    while(aboveErr):
        epochResults = []
        for j in range(len(lettersInput)):
            result = ml.trainLayers(
                InputVector(lettersInput[j]._x, ord(lettersInput[j]._letter))
            )
            # here result is the final answer from the net for certain letter
            epochResults.append(result)

        mseVal = MSE(epochResults, expectedForAllLetters)
        if mseVal < 0.001:
            aboveErr = False
        epoch += 1
        if epoch % 10 == 0:
            print('epoch: ', epoch, "\tMSE err: " , mseVal)


    """ TESTING """
    print('\n')
    lettersInput.append(LetterInput('a_noised')) # Letter unknown to the net
    lettersInput.append(LetterInput('D_noised'))
    table = PrettyTable()
    table.field_names = ['Letter', 'PREDICTED', 'RAW RESULT (ASCII)']
    for letter in lettersInput:
        result = ml.processLayers(letter['x'])
        table.add_row([letter._letter, chr(int(round(result))), result])
    print(table)
