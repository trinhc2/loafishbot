import cv2 as cv
import numpy as np
import os
import pyautogui
import time
import random
import keyboard
from windowcapture import WindowCapture

# venv is outside of this folder so this changes the working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
wincap = WindowCapture('LOST ARK (64-bit, DX11) v.3.1.2.1')
partialImage = cv.imread('partial.jpg', cv.IMREAD_UNCHANGED)
# WindowCapture.listWindows()
botStarted = False
fishingKey = 'e'
fishingPosX = 0
fishingPosY = 0
fishCaught = 0
matchingThreshold = 0.9


def repairTool():
    remoteRepairMin = [1218, 710]
    remoteRepairMax = [1238, 719]
    repairAllMin = [564, 785]
    repairAllMax = [892, 822]
    okayMin = [861, 615]
    okayMax = [952, 639]

    pyautogui.hotkey('alt', 'p')
    pyautogui.moveTo(random.uniform(remoteRepairMin[0], remoteRepairMax[0]),
                     random.uniform(remoteRepairMin[1], remoteRepairMax[1]),
                     0.5)
    pyautogui.click()
    time.sleep(random.uniform(1, 2))
    pyautogui.moveTo(random.uniform(repairAllMin[0], repairAllMax[0]),
                     random.uniform(repairAllMin[1], repairAllMax[1]),
                     0.5)
    pyautogui.click()
    pyautogui.moveTo(random.uniform(okayMin[0], okayMax[0]),
                     random.uniform(okayMin[1], okayMax[1]),
                     0.5)
    pyautogui.click()
    time.sleep(random.uniform(0.5, 1))
    pyautogui.press('esc')
    time.sleep(random.uniform(0.5, 1))
    pyautogui.press('esc')
    pass


def checkStopScript():
    if keyboard.is_pressed('ctrl+q'):  # Check for Ctrl + Q globally
        print("Stopping script...")
        exit()
    pass


print("Waiting for user to begin fishing...")

while (not botStarted):
    if keyboard.is_pressed(fishingKey):
        print("Bot started. Press Ctrl+Q to stop at any time.")
        fishingPosX, fishingPosY = pyautogui.position()
        botStarted = True


while (botStarted):
    checkStopScript()
    # get an updated image of the game
    screenshot = wincap.getScreenshot()
    # screenshot = np.copy(screenshot)

    result = cv.matchTemplate(
        screenshot, partialImage, cv.TM_CCOEFF_NORMED)
    minVal, maxMatchValue, minLoc, maxLoc = cv.minMaxLoc(result)

    # cv.imshow('Computer Vision', screenshot)
    # print(maxVal)
    if maxMatchValue >= matchingThreshold:
        print("found")
        pyautogui.press(fishingKey)
        time.sleep(random.uniform(6, 7.5))
        fishCaught += 1
        if fishCaught >= 5:
            repairTool()
            pyautogui.moveTo(fishingPosX, fishingPosY, 0.5)
            fishCaught = 0
        pyautogui.press(fishingKey)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
'''
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
'''
