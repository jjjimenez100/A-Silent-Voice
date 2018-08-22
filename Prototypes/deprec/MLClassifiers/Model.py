import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class Model:
    def __init__(self, dataset: str):
        self.__scaler = StandardScaler()
        self.__dataset = pandas.read_csv(dataset)

    def __scaleFeatures(self):
        self.__removeLabels = self.__dataset.drop("label", axis=1)
        self.__scaler.fit(self.__removeLabels)
        self.__scaledFeatures = self.__scaler.transform(self.__removeLabels)
        self.__flatFeatures = pandas.DataFrame(self.__scaledFeatures, columns=self.__dataset.columns[1:])

    def __trainTestSplit(self, testSize: int=3, randomState: int=101):
        self.__features = self.__flatFeatures
        self.__predictionLabels = self.__dataset["label"]
        self.__xTrain, self.__xTest, self.__yTrain, self.__yTest \
            = train_test_split(self.__features, self.__predictionLabels,test_size=testSize, random_state=randomState)

    def createClassifier(self):
        pass

    def __fitDataToClassifier(self):
        self.classifier.fit(self.__xTrain, self.__yTrain)

    def getPrediction(self, values):
        return self.classifier.predict(values)

    def preprocessData(self):
        self.__scaleFeatures()
        self.__trainTestSplit()
        self.createClassifier()
        self.__fitDataToClassifier()

    def saveModel(self, savePath: str="", compressSize: int=9):
        from sklearn.externals import joblib
        joblib.dump(self.classifier, savePath, compress=compressSize)