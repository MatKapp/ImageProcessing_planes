import os
import re
from os import listdir
from os.path import isfile, join

import numpy as np
from matplotlib import pyplot as plt
from skimage import data, measure, filters
from skimage.exposure import exposure
from skimage.filters import scharr


def findNamesOfPictures():
    mypath = os.path.dirname(os.path.realpath(__file__))
    onlyFiles= [f for f in listdir(mypath) if isfile(join(mypath, f))]
    nameOfImagesToProcessing=[]
    for fileName in onlyFiles:

            if re.match("^samolot...jpg$", fileName):
                nameOfImagesToProcessing.append(fileName)

    return nameOfImagesToProcessing


def showImages(images, contours):
    print("wypisuje zdjecia")
    fig, axes = plt.subplots(5, 5, figsize=(10,10), sharex= True, sharey= True)
    ax = axes.ravel();
    for i in range(len(images)):
        ax[i].imshow(images[i], interpolation="nearest", extent=[-2, 4, -2, 4], cmap="gray")
        ax[i].set_title(imageNames[i])
        ax[i].axis('off')
        for n, contour in enumerate(contours[i]):
            if n > 10:
                break
            temp = contour
            ax[i].plot(temp[:, 1], temp[:, 0], linewidth=1)

    plt.savefig('test.pdf')


def findContours(images):
    result = []
    for i in range(len(images)):
        p2, p98 = np.percentile(images[i], (0, 95))
        images[i] = exposure.rescale_intensity(images[i], in_range=(p2, p98))

        images[i] = scharr(images[i])
        images[i] = filters.sobel(images[i])
        result.append(measure.find_contours(images[i], level=0.14, fully_connected="high", positive_orientation="high"))

    # result= measure.find_contours(images[0], level=0.7)
    return result


def loadImages(names):
    result = []
    for i in range(len(names)):
        result.append(data.imread(names[i], as_grey=True))
    return result



if __name__ == "__main__":
    imageNames = findNamesOfPictures()
    imageCollection = loadImages(imageNames)
    contours = findContours(imageCollection)
    showImages(imageCollection, contours)
