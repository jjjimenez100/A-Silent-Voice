import tensorflow as tf
import numpy as np
class TFModel:
    def __init__(self, modelPath: str, labelPath: str, inputLayer: str, outputLayer: str):
        self.modelFile = modelPath
        self.labelFile = labelPath
        self.inputLayer = inputLayer
        self.outputLayer = outputLayer
        self.inputHeight = 299
        self.inputWidth = 299
        self.inputMean = 0
        self.inputStd = 255
        self.graph = self.loadGraph()
        self.labels = self.loadLabels()
        self.inputNameLayer = "import/" + self.inputLayer
        self.outputNameLayer = "import/" + self.outputLayer
        self.inputOperation = self.graph.get_operation_by_name(self.inputNameLayer)
        self.outputOperation = self.graph.get_operation_by_name(self.outputNameLayer)

    def loadGraph(self):
        graph = tf.Graph()
        graphDef = tf.GraphDef()

        with open(self.modelFile, "rb") as f:
            graphDef.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graphDef)

        return graph

    def readTensor(self, imagePath: str):
        inputName = "file_reader"
        fileReader = tf.read_file(imagePath, inputName)
        if imagePath.endswith(".png"):
            imageReader = tf.image.decode_png(
                fileReader, channels=3, name="png_reader")
        elif imagePath.endswith(".gif"):
            imageReader = tf.squeeze(
                tf.image.decode_gif(fileReader, name="gif_reader"))
        elif imagePath.endswith(".bmp"):
            imageReader = tf.image.decode_bmp(fileReader, name="bmp_reader")
        else:
            imageReader = tf.image.decode_jpeg(
                fileReader, channels=3, name="jpeg_reader")
        castToFloat = tf.cast(imageReader, tf.float32)
        expandDims = tf.expand_dims(castToFloat, 0)
        resized = tf.image.resize_bilinear(expandDims, [self.inputHeight, self.inputWidth])
        normalized = tf.divide(tf.subtract(resized, [self.inputMean]), [self.inputStd])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    def loadLabels(self):
        labels = []
        asciiLines = tf.gfile.GFile(self.labelFile).readlines()
        for line in asciiLines:
            labels.append(line.rstrip())

        return labels

    def predict(self, imagePath: str):
        tensor = self.readTensor(imagePath)
        with tf.Session(graph=self.graph) as sess:
            results = sess.run(self.outputOperation.outputs[0], {
                self.inputOperation.outputs[0]: tensor
            })
        results = np.squeeze(results)
        topResults = results.argsort()[-1:][::-1]
        for i in topResults:
            print(self.labels[i], results[i])