from random import shuffle
import os
import argparse

def randomize(location):

    imageList = []
    renamed = []
    foldercount = 0

    for p, d, f in os.walk(location):
        list = []
        for j in f:
            list.append(p+"/"+j)
        imageList.append(list)

    imageList.__delitem__(0)
    for i in imageList:
        shuffle(i)

    for j in range(len(imageList)):
        list = []
        for i in range(len(imageList[j])):
            rename = "/".join(imageList[j][i].split("/")[:-1])+"/"+str(i+len(imageList[j]))+".jpg"
            list.append(rename)
            os.rename(imageList[j][i], rename)
        renamed.append(list)

    for j in range(len(renamed)):
        for i in range(len(renamed[j])):
            print("renaming",renamed[j][i], "/".join(imageList[j][i].split("/")[:-1])+"/"+str(i)+".jpg")
            os.rename(renamed[j][i], "/".join(imageList[j][i].split("/")[:-1])+"/"+str(i)+".jpg")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", help="Location of dataset files") #python NameRandomizer.py --location "C:\Dataset Aug 3\"
    args = parser.parse_args()
    loc = ''
    if args.location:
        loc = args.location
    randomize(loc)