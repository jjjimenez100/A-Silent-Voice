import Modules.CNN.TFModel as tf
import os

imageLocation = r'C:\School\thesis\jols frames\greyscale'

output = {"A": [0, 0], "B": [0, 0], "C": [0, 0], "D": [0, 0], "E": [0, 0]
        , "F": [0, 0], "G": [0, 0], "H": [0, 0], "I": [0, 0], "J": [0, 0]
        , "K": [0, 0], "L": [0, 0], "M": [0, 0], "N": [0, 0], "O": [0, 0]
        , "P": [0, 0], "Q": [0, 0], "R": [0, 0], "S": [0, 0], "T": [0, 0]
        , "U": [0, 0], "V": [0, 0], "W": [0, 0], "X": [0, 0], "Y": [0, 0]
        , "Z": [0, 0]}
total = 0

model = tf.TFModel("output_graph.pb", "output_labels.txt", "Placeholder", "final_result")

for path, directory, file in os.walk(imageLocation):
    print(path, directory, file)
    for i in directory:
        for p, d, f in os.walk(path+"/"+i+"/"):
            filec = len(f)
            for j in f:
                letter, acc = model.classifyImage(path+"/"+i+"/"+j)
                if letter.upper() == i:
                    output[i][0] += 1
                else:
                    with open('failed_imgs.txt', 'a') as file:
                        file.write(i+"/"+j+"\n")
                output[i][1] += 1
                total+=1


print(output)
with open('output.txt', 'a') as file:
    from datetime import datetime
    file.write(str(datetime.today()))
    for i in output:
        try:
            percentage = str((output[i][0]/output[i][1]*100)) + "%"
        except:
            percentage = str(0)+"%"
        file.write("\n"+i+" - "+percentage)