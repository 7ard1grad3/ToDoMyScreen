import cv2
import pytesseract
from mss import mss

from config import *


class ScreenCapture:

    @staticmethod
    def take_screen_shot():
        # Read image
        with mss() as sct:
            filename = sct.shot(mon=-1, output=FULL_SCREEN_IMAGE_PATH)
        # Get the cv2 image object
        image = cv2.imread(filename)
        return image

    @staticmethod
    def crop_image(cv2_image):
        # Select ROI
        r = cv2.selectROI("Image", cv2_image, False, False)
        r.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        cv2.destroyWindow("Image")
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

    @staticmethod
    def make_screen_shot():
        screen_shot = ScreenCapture.take_screen_shot()
        cropped = ScreenCapture.crop_image(screen_shot)
        text = ScreenCapture.read_text_from_image(cropped)
        print(text)
