from sklearn.utils import shuffle
import pickle
from Modules.CNN.Constants import *
from Modules.OpenCVWrapper import *

def getImages():
    images = []
    for label in os.listdir(GESTURES_PATH):
        for index in range(TRAIN_IMAGES_SIZE):
            fileName = GESTURES_PATH + "/" + label + "/" + str(index+1) + IMAGE_FILE_FORMAT
            print("Current image: %s" %fileName)
            image = loadImage(fileName, 0)
            # Check if image loaded is null
            if(numpy.any(image == None)):
                continue
            images.append(image)

    return images

def splitImagesAndLabels(images):
    extractedImages = []
    extractedLabels = []
    for (extractedImage, extractedLabel) in images:
        extractedImages.append(extractedImage)
        extractedLabels.append(extractedLabel)

    return [extractedImages, extractedLabels]

def createDataset():
    images = shuffle(shuffle(shuffle(shuffle(shuffle(getImages())))))
    extractedImages, extractedLabels = splitImagesAndLabels(images)
    print("Number of images on dataset: %d" %len(extractedImages))

    trainImagesSet = extractedImages[:int(5 / 6 * len(images))]
    print("Length of train_images", len(trainImagesSet))
    with open("train_images", "wb") as file:
        pickle.dump(trainImagesSet, file)
    del trainImagesSet

    trainLabelsSet = extractedLabels[:int(5 / 6 * len(extractedLabels))]
    print("Length of train_labels", len(trainLabelsSet))
    with open("train_labels", "wb") as file:
        pickle.dump(trainLabelsSet, file)
    del trainLabelsSet

    testImagesSet = extractedImages[int(5 / 6 * len(images)):]
    print("Length of test_images", len(testImagesSet))
    with open("test_images", "wb") as file:
        pickle.dump(testImagesSet, file)
    del testImagesSet

    testLabelsSet = extractedLabels[int(5 / 6 * len(extractedLabels)):]
    print("Length of test_labels", len(testLabelsSet))
    with open("test_labels", "wb") as file:
        pickle.dump(testLabelsSet, file)
    del testLabelsSet

    print("Dataset dumping = done.")

createDataset()
