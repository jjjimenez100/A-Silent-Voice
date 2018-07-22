MODEL_PATH = "D:\GitHub\A-Silent-Voice\cnn_model_keras2.h5"
MODEL_VISUALIZATION_PATH = "CnnModel.png"
TRAIN_IMAGES_PATH = "trainImages.dataset"
TRAIN_LABELS_PATH = "trainLabels.dataset"
TEST_IMAGES_PATH = "testImages.dataset"
TEST_LABELS_PATH = "testLabels.dataset"
GESTURES_PATH = "gestures"

TRAIN_IMAGES_SIZE = 2400
IMAGE_FILE_FORMAT = ".jpg"
TRAIN_SET_SIZE = int(5/6*TRAIN_IMAGES_SIZE)

IMAGE_WIDTH = 50
IMAGE_HEIGHT = 50

LABELS = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
LABELS.extend("0 1 2 3 4 5 6 7 8 9".split(" "))
LABELS.extend(["Best of Luck", "You", "I", "Like", "Remember", "Love", "Fuck", "I Love You"])
