import os
import re
from os import listdir
from os.path import isfile, join

import cv2
import numpy as np
from matplotlib import pyplot as plt


def findNamesOfPictures():
    mypath = os.path.dirname(os.path.realpath(__file__))
    onlyFiles= [f for f in listdir(mypath) if isfile(join(mypath, f))]
    nameOfImagesToProcessing=[]
    for fileName in onlyFiles:

            if re.match("^samolot...jpg$", fileName):
                nameOfImagesToProcessing.append(fileName)

    return nameOfImagesToProcessing


def showImages(images):
    print("wypisuje zdjecia")
    fig, axes = plt.subplots(5, 5, figsize=(10,10), sharex= True, sharey= True)
    ax = axes.ravel();
    for i in range(len(images)):
        ax[i].imshow(images[i], interpolation="nearest", extent=[-2, 4, -2, 4])
        ax[i].set_title(imageNames[i])
        ax[i].axis('off')
        # for n, contour in enumerate(contours[i]):
        #     if n > 10:
        #         break
        #     temp = contour
        #     ax[i].plot(temp[:, 1], temp[:, 0], linewidth=1)

    plt.savefig('test.pdf')


def findContours(images):
    result = []

    # result= measure.find_contours(images[0], level=0.7)
    return result


def loadImages(names):
    result = []
    for i in range(len(names)):
        result.append(cv2.imread(names[i], cv2.IMREAD_COLOR))
    return result


def rgbBgrConversion(images):
    result = []
    for i in range(len(images)):
        temp = images[i]
        temp = temp[:, :, ::-1]
        result.append(temp)
    return result



if __name__ == "__main__":
    imageNames = findNamesOfPictures()
    imageCollection = loadImages(imageNames)
    imageCollection = np.array(imageCollection)
    print(type(imageCollection))
    print(imageCollection[0].shape)
    imageCollection = rgbBgrConversion(imageCollection)
    # contours = findContours(imageCollection)
    showImages(imageCollection)
