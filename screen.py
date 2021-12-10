import os

import cv2
import pytesseract
from mss import mss

from config import *
from todo import ToDo


class ScreenCapture:

    def __init__(self, to_do: ToDo):
        self.to_do = to_do

    @staticmethod
    def full_screen_shot():
        # Read image
        with mss() as sct:
            filename = sct.shot(mon=-1, output=FULL_SCREEN_IMAGE_PATH)
        # Get the cv2 image object
        image = cv2.imread(filename)
        return image

    @staticmethod
    def crop_image(cv2_image):
        # Select ROI
        window_name = "image"
        cv2.imshow(window_name, cv2_image)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 1)
        cv2.setWindowProperty(window_name, cv2.WINDOW_AUTOSIZE, 1)
        r = cv2.selectROI("image", cv2_image, False)

        cv2.waitKey(1)
        cv2.destroyWindow("image")
        # Crop image
        imCrop = cv2_image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # Save the cropped image
        try:
            cv2.imwrite(CROPPED_IMAGE_PATH, imCrop)
        except:
            pass
        image = cv2.imread(CROPPED_IMAGE_PATH)
        return image

    @staticmethod
    def read_text_from_image(cv2_image):
        return pytesseract.image_to_string(cv2_image)

    def capture_screen(self):
        screen_shot = ScreenCapture.full_screen_shot()
        cropped = ScreenCapture.crop_image(screen_shot)
        text = ScreenCapture.read_text_from_image(cropped)
        if text != "":
            self.to_do.add_task(text, os.getenv('TODO_LIST_ID'))
