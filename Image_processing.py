from os import listdir
import os
from os.path import isfile, join
from skimage import data, io
from matplotlib import pyplot as plt
import re


def findNamesOfPictures():
    mypath = os.path.dirname(os.path.realpath(__file__))
    onlyFiles= [f for f in listdir(mypath) if isfile(join(mypath, f))]
    nameOfImagesToProcessing=[]
    for fileName in onlyFiles:

            if re.match("^samolot...jpg$", fileName):
                nameOfImagesToProcessing.append(fileName)

    return nameOfImagesToProcessing


def showImages():
    fig, axes = plt.subplots(5, 5, figsize=(10,10), sharex= True, sharey= True)
    ax = axes.ravel();
    for i in range (len(imageCollection)):
        ax[i].imshow(imageCollection[i], aspect="auto", interpolation="nearest")
        ax[i].set_title(imageNames[i])
        ax[i].axis('off')
    plt.savefig('test.pdf')


if __name__ == "__main__":
    imageNames = findNamesOfPictures()
    imageCollection = io.ImageCollection(imageNames)
    showImages()