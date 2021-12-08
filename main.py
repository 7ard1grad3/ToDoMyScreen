from pynput.keyboard import Listener
from pytesseract import pytesseract

from config import PYTESSERACT_PATH
from keyboard import KeyboardListener

if __name__ == '__main__':
    # Init global path for pytesseract
    pytesseract.tesseract_cmd = PYTESSERACT_PATH
    keyboardListener = KeyboardListener()
    with Listener(on_press=keyboardListener.on_press, on_release=keyboardListener.on_release) as listener:
        listener.join()
