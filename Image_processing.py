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


def findContours(images):
    result = []
    goodContours = []
    for i in range (len (images)):
        # ret, thresh = cv2.threshold (images[i], 127, 255, 0)
        image, contours, hierarchy = cv2.findContours (np.array (images[i]), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for j in range (len (contours)):
            print (cv2.contourArea (contours[j]))
            if (cv2.contourArea (contours[j]) > 100000):
                goodContours.append (contours[j])
        result.append (goodContours)
    return result


def drawContours(images, contours):
    result = []
    for i in range (len (images)):
        print (type (np.array (contours[i])))
        print ((np.array (contours[i])).shape)
        result.append (cv2.drawContours (np.array (images[i]), np.array (contours[i]), -1, (155, 155, 155), 1))
    return result


def showImages(images):
    print("wypisuje zdjecia")
    fig, axes = plt.subplots(5, 5, figsize=(10,10), sharex= True, sharey= True)
    ax = axes.ravel();
    for i in range(len(images)):
        ax[i].imshow(images[i], interpolation="nearest", extent=[-2, 4, -2, 4], cmap="gray")
        ax[i].set_title(imageNames[i])
        ax[i].axis('off')
        # for n, contour in enumerate(contours[i]):
        #     if n > 10:
        #         break
        #     temp = contour
        #     ax[i].plot(temp[:, 1], temp[:, 0], linewidth=1)

    plt.savefig('test.pdf')


def loadImages(names):
    result = []
    for i in range(len(names)):
        result.append(cv2.imread(names[i], cv2.IMREAD_GRAYSCALE))
    return result


def rgbBgrConversion(images):
    result = []
    for i in range(len(images)):
        temp = images[i]
        temp = temp[:, :, ::-1]
        result.append(temp)
    return result


def denoisingImages(images):
    result = []
    for i in range(len(images)):
        temp = images[i]
        kernel = np.ones ((5, 5), np.uint8)
        temp = cv2.fastNlMeansDenoising(temp, h=10, templateWindowSize=7, searchWindowSize=21)
        temp = cv2.morphologyEx (temp, cv2.MORPH_OPEN, kernel)
        result.append(temp)
    return result


def filteringImages(images):
    result = []
    for i in range(len(images)):
        temp = images[i]

        # hist, bins = np.histogram (temp, 256, [0, 256])
        # cdf = hist.cumsum ()
        # cdf_normalized = cdf * hist.max () / cdf.max ()
        # cdf_m = np.ma.masked_equal (cdf, 0)
        # cdf_m = (cdf_m - cdf_m.min ()) * 255 / (cdf_m.max () - cdf_m.min ())
        # cdf = np.ma.filled (cdf_m, 0).astype ('uint8')
        # temp=cdf[temp]



        blur = cv2.GaussianBlur (temp, (5, 5), 0)
        ret2, temp = cv2.threshold (blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # temp = cv2.adaptiveThreshold (temp, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                             cv2.THRESH_BINARY, 11, 2)
        #temp = cv2.Canny(temp, 50, 550, L2gradient=True)


        result.append(temp)
    return result


def gamma_correction(img, correction):
    img = img / 255.0
    img = cv2.pow (img, correction)
    return np.uint8 (img * 255)


def filteringImages2(images):
    result = []
    for i in range (len (images)):
        temp = images[i]

        gamma = 0.5
        kernel = np.ones ((5, 5), np.uint8)

        temp = cv2.medianBlur (temp, 5)
        temp = gamma_correction (temp, gamma)
        temp = cv2.Laplacian (temp, cv2.CV_8UC1)
        temp = cv2.dilate (temp, kernel, iterations=5)
        temp = cv2.erode (temp, kernel, iterations=2)
        # temp=cv2.bitwise_not(temp)
        # hist, bins = np.histogram (temp, 256, [0, 256])
        # cdf = hist.cumsum ()
        # cdf_normalized = cdf * hist.max () / cdf.max ()
        # cdf_m = np.ma.masked_equal (cdf, 0)
        # cdf_m = (cdf_m - cdf_m.min ()) * 255 / (cdf_m.max () - cdf_m.min ())
        # cdf = np.ma.filled (cdf_m, 0).astype ('uint8')
        # temp=cdf[temp]

        # blur = cv2.GaussianBlur (temp, (5, 5), 0)
        # ret2, temp = cv2.threshold (blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # temp= cv2.Canny(temp, 100, 200)

        # temp= morphology.binary_fill_holes(temp)
        result.append (temp)
    return result


if __name__ == "__main__":
    imageNames = findNamesOfPictures()
    imageCollection = loadImages(imageNames)
    imageCollection = np.array(imageCollection)
    imageCollection = denoisingImages (imageCollection)
    imageCollection = filteringImages2 (imageCollection)

    # contours = findContours (imageCollection)
    # imageCollection = drawContours(imageCollection, contours)


    showImages(imageCollection)
