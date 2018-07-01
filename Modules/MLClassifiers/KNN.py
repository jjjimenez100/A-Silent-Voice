from Algorithms.MachineLearning.Model import Model
from sklearn.neighbors import KNeighborsClassifier

class KNN(Model):
    def __init__(self, dataSet: str, kValue: int=3):
        Model.__init__(self, dataSet)
        self.kValue = kValue
        self.preprocessData()

    def createClassifier(self):
        self.classifier = KNeighborsClassifier(n_neighbors=self.kValue)