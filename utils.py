from copy import deepcopy

import cv2
import numpy as np


def getSharpness(i):
    kernelSize = 3
    convX = cv2.Sobel(cv2.cvtColor(i, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 1, 0, ksize=kernelSize)
    convY = cv2.Sobel(cv2.cvtColor(i, cv2.COLOR_BGR2GRAY), cv2.CV_64F, 1, 0, ksize=kernelSize)
    tempArrX = deepcopy(convX * convX)
    tempArrY = deepcopy(convY * convY)
    tempSumXY = tempArrX + tempArrY
    tempSumXY = np.sqrt(tempSumXY)
    sharpness = np.sum(tempSumXY)
    return sharpness

def getBestSharpnessIndex(imgs,x1, x2,y1, y2):
    bestIndex = -1
    bestSharpness = -1
    for k in range(imgs.shape[0]):
        im = deepcopy(imgs[k])
        sharpness = getSharpness(im[x1:x2, y1:y2])
        if (bestSharpness < sharpness):
            bestIndex = k
            bestSharpness = sharpness
    return bestIndex