import cv2 as cv
import numpy as np
import os
import sys
import pyautogui
import time
import random
import keyboard
from windowcapture import WindowCapture

if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
    app_path = sys._MEIPASS  # Get the temporary folder where PyInstaller extracts files
else:
    app_path = os.path.dirname(os.path.realpath(
        __file__))  # Use the script's directory

# Load image with the correct path
fishCaughtImage = cv.imread(os.path.join(
    app_path, 'src', 'caughtFish.jpg'), cv.IMREAD_UNCHANGED)
damagedToolImage = cv.imread(os.path.join(
    app_path, 'src', 'damagedTool.jpg'), cv.IMREAD_UNCHANGED)

# venv is outside of this folder so this changes the working directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
wincap = WindowCapture('LOST ARK (64-bit, DX11) v.3.1.2.1')
# WindowCapture.listWindows()
botStarted = False
fishingKey = 'e'
fishingPosX = 0
fishingPosY = 0
fishCaught = 0
matchingThreshold = 0.9
idleTimer = 0


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
    time.sleep(random.uniform(1, 2))
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
        print(f'Total fish caught: {fishCaught}')
        sys.exit()
    pass


print("Waiting for user to begin fishing...")

try:
    while (not botStarted):
        checkStopScript()
        if keyboard.is_pressed(fishingKey):
            print("Bot started. Press Ctrl+Q to stop at any time.")
            fishingPosX, fishingPosY = pyautogui.position()
            botStarted = True

    while (botStarted):
        checkStopScript()

        idleTimer += 1
        if idleTimer >= 500:
            print("Idle for too long, out of energy? Stopping script")
            exit()

        screenshot = wincap.getScreenshot()

        checkFishing = cv.matchTemplate(
            screenshot, fishCaughtImage, cv.TM_CCOEFF_NORMED)
        minVal, maxMatchValue, minLoc, maxLoc = cv.minMaxLoc(checkFishing)

        if maxMatchValue >= matchingThreshold:
            print("found")
            pyautogui.press(fishingKey)  # reel in fish
            time.sleep(random.uniform(6, 7.5))
            fishCaught += 1
            if fishCaught % 10 == 0:
                print("checking tool durability")
                checkTool = cv.matchTemplate(
                    screenshot, damagedToolImage, cv.TM_CCOEFF_NORMED)
                minVal, maxMatchValue, minLoc, maxLoc = cv.minMaxLoc(checkTool)
                if maxMatchValue >= 0.60:
                    print("Damaged tool detected. Repairing")
                    repairTool()
                    pyautogui.moveTo(fishingPosX, fishingPosY, 0.5)
            print("casting")
            pyautogui.press(fishingKey)  # recast line
            idleTimer = 0

except KeyboardInterrupt:
    print("Exit by keyboard")
