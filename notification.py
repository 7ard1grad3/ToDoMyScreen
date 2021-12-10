import sys
from sys import platform

from win10toast import ToastNotifier


class Notification:
    @staticmethod
    def send_notification(message, exit=False, duration=5):
        if platform == "win32":
            ToastNotifier().show_toast("Shed ToDo", message, duration=duration,
                                       icon_path="app.ico")
        elif platform == "linux" or platform == "linux2":
            if not exit:
                print(message)
        if exit:
            sys.exit(message)
