from dotenv import load_dotenv
from pynput.keyboard import Listener
from pytesseract import pytesseract

from config import PYTESSERACT_PATH
from keyboard import KeyboardListener
from screen import ScreenCapture
from todo import ToDo

if __name__ == '__main__':
    load_dotenv()

    tasks = ToDo()
    # Init global path for pytesseract
    pytesseract.tesseract_cmd = PYTESSERACT_PATH
    keyboardListener = KeyboardListener(ScreenCapture(tasks))
    with Listener(on_press=keyboardListener.on_press, on_release=keyboardListener.on_release) as listener:
        listener.join()
