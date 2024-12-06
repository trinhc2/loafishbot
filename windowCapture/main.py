import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture

# venv is outside of this folder so this changes the working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

wincap = WindowCapture('Lost Ark 2024.12.04 - 15.20.14.02.DVR.mp4')

partialImage = cv.imread('partial.jpg', cv.IMREAD_UNCHANGED)

while (True):

    # get an updated image of the game
    screenshot = wincap.getScreenshot()
    screenshot = np.copy(screenshot)

    result = cv.matchTemplate(screenshot, partialImage, cv.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)
    # cv.imshow('Computer Vision', screenshot)
    # print(maxVal)
    threshold = 0.9
    if maxVal >= threshold:
        print("found")

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
