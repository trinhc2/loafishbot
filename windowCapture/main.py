import cv2 as cv
import numpy as np
import os
import pyautogui
import time
import random
import keyboard
from windowcapture import WindowCapture

'''
1218,710 / 1238,719 -> remote repair
564,785 / 892 822 -> repair all
861,615 / 952 639 -> okay button
'''

# venv is outside of this folder so this changes the working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

wincap = WindowCapture('LOST ARK (64-bit, DX11) v.3.1.2.1')

partialImage = cv.imread('partial.jpg', cv.IMREAD_UNCHANGED)
# WindowCapture.listWindows()

botStarted = False
fishingKey = 'e'

print("Waiting for user to begin fishing...")

while (not botStarted):
    if keyboard.is_pressed(fishingKey):
        print("Bot started. Press Ctrl+C to stop at any time.")
        # botStarted = True
    print(pyautogui.position())

try:
    while (botStarted):
        # get an updated image of the game
        screenshot = wincap.getScreenshot()
        screenshot = np.copy(screenshot)

        result = cv.matchTemplate(
            screenshot, partialImage, cv.TM_CCOEFF_NORMED)
        minVal, maxMatchValue, minLoc, maxLoc = cv.minMaxLoc(result)
        cv.imshow('Computer Vision', screenshot)
        # print(maxVal)
        matchingThreshold = 0.9
        if maxMatchValue >= matchingThreshold:
            print("found")
            pyautogui.press(fishingKey)
            time.sleep(random.uniform(6, 7.5))
            pyautogui.press(fishingKey)

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

except KeyboardInterrupt:
    print("Bot stopped.")
