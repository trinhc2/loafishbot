import numpy as np
import win32gui
import win32ui
import win32con


class WindowCapture:

    w = 0
    h = 0
    hwnd = None

    def __init__(self, window_name) -> None:
        self.h = 1080
        self.w = 1920
        self.hwnd = win32gui.FindWindow(None, window_name)

    def getScreenshot(self):
        # Get the device context for the window
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        # Create a compatible bitmap and select it into the device context
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # Copy the window content into the bitmap
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY)

        # Get the raw bitmap data
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype=np.uint8)

        # Reshape the array to the appropriate image dimensions
        img = img.reshape(self.h, self.w, 4)  # Assuming 32-bit RGBA format
        # Remove the alpha channel if present (convert to RGB)
        img = img[..., :3]

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # Return the image as a NumPy array compatible with OpenCV
        return img

    @staticmethod
    def listWindows():
        def getOpenWindows(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(getOpenWindows, None)
