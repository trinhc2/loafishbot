import cv2 as cv
import numpy as np
import os

#venv is outside of this folder so this changes the working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

fullImage = cv.imread('full.jpg', cv.IMREAD_UNCHANGED)
partialImage = cv.imread('partial.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(fullImage, partialImage, cv.TM_CCOEFF_NORMED)

minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)

threshold = 0.8
if maxVal >= threshold:
    partialImageWidth = partialImage.shape[1]
    partialImageHeight = partialImage.shape[0]

    topLeft = maxLoc
    bottomRight = (topLeft[0] + partialImageWidth, topLeft[1] + partialImageHeight)

    cv.rectangle(fullImage, topLeft, bottomRight, 255, 2)

    cv.imshow('Result', fullImage)
    cv.waitKey()

else:
    print("Not Found")