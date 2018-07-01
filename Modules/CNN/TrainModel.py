from keras import backend as K
from Modules.OpenCVWrapper import *
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from Modules.CNN.Constants import *
import numpy
import pickle


def getImageSize():
    return loadImage(TRAIN_IMAGES_PATH+"/0/1.jpg").shape

# Tensorflow backend
K.set_image_dim_ordering("tf")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"

imageWidth, imageHeight = getImageSize()

def getNumberOfLabels():
    return len(os.listdir(TRAIN_IMAGES_PATH))

def cnnModel():
    numberOfLabels = getNumberOfLabels()

    # Create a sequential stack of layers.
    cnnModel = Sequential()
    cnnModel.add(Conv2D(16, (2, 2), input_shape=(imageWidth, imageHeight, 1), activation='relu'))
    cnnModel.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    cnnModel.add(Conv2D(32, (5, 5), activation='relu'))
    cnnModel.add(MaxPooling2D(pool_size=(5, 5), strides=(5, 5), padding='same'))
    cnnModel.add(Conv2D(64, (5, 5), activation='relu'))
    cnnModel.add(Flatten())
    cnnModel.add(Dense(128, activation='relu'))
    cnnModel.add(Dropout(0.2))
    cnnModel.add(Dense(numberOfLabels, activation='softmax'))
    sgd = optimizers.SGD(lr=1e-2)
    cnnModel.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    trainingCheckpoint = ModelCheckpoint(MODEL_PATH, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbackList = [trainingCheckpoint]

    from keras.utils import plot_model
    plot_model(cnnModel, to_file='model.png', show_shapes=True)

    return cnnModel, callbackList

def loadData(strPath: str, fileAccessMode: str="rb", dType=None):
    with open(strPath, fileAccessMode) as file:
        return numpy.array(pickle.load(file, dType))

def processDataset():
    trainImages = loadData(TRAIN_IMAGES_PATH)
    testImages = loadData(TEST_IMAGES_PATH)
    trainImages = trainImages.reshape(trainImages, (trainImages.shape, imageWidth, imageHeight, 1))
    testImages = testImages.reshape(testImages, (testImages.shape, imageWidth, imageHeight, 1))

    trainLabels = loadData(TRAIN_LABELS_PATH)
    testLabels = loadData(TEST_LABELS_PATH)
    trainLabels = np_utils.to_categorical(trainLabels)
    testLabels = np_utils.to_categorical(testLabels)

    return [trainImages, trainLabels, testImages, testLabels]

def trainCnnModel():
    dataSet = processDataset()
    model, callbackList = cnnModel()
    # Print training summary
    model.summary()
    model.fit(dataSet[0], dataSet[1], validation_data=(dataSet[2], dataSet[3]), epochs=20, batch_size=500, callbacks=callbackList)
    predictionScores = model.evaluate(dataSet[2], dataSet[3], verbose=0)
    print("Error rate is: %0.2f" % (100-predictionScores[1]*100))

trainCnnModel()
K.clear_session()