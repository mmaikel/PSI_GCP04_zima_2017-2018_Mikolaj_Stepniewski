from keras.models import Sequential
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense
from keras import optimizers
from prettytable import PrettyTable
from rastrigin import *
from model import *


""" Parameters """
lRate = 0.05
layers = [30, 1]
numberOfInputs = 2000
epochs = 200
batchSize = 20
decay = 0


""" Initializing training data """
trainingData = RastriginInput()
trainingData.initRastriginPointsRand(numberOfInputs)
trainingDataInput = trainingData.getInputArray()
trainingDataExpectedOutput = trainingData.getOutputArray()

""" Initializing validation data """
validationData = RastriginInput()
validationData.initRastriginPoints(0.5)
valDataOutput = validationData.getOutputArray()
valDataInput = validationData.getInputArray()

""" Initializing Tensor Board, which contains charts, histograms etc.  """
tensorBoard = TensorBoard(  log_dir='./logs',
                            histogram_freq=5,
                            batch_size=20,
                            write_graph=True,
                            write_grads=False,
                            write_images=True,
                            embeddings_freq=0,
                            embeddings_layer_names=None,
                            embeddings_metadata=None
)

""" Saves weights of the model """
checkpointer = ModelCheckpoint(filepath='./checkpoints/weights.hdf5', verbose=1, save_best_only=True)



""" Keras Model """
kModel = KerasModel(layers, [tensorBoard, checkpointer])
kModel.createModel()
kModel.train(
    lRate,
    decay,
    trainingDataInput,
    trainingDataExpectedOutput,
    epochs,
    batchSize,
    (valDataInput, valDataOutput)
)

""" Summary table """
print('\n\n\tSummary:\n', kModel._model.summary())
kModel.printEvaluation(valData=[valDataInput, valDataOutput])
