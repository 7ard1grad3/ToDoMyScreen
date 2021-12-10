from pynput.keyboard import Key

from screen import ScreenCapture


class KeyboardListener:
    def __init__(self, screen_capture: ScreenCapture):
        # The currently pressed keys (initially empty)
        self.pressed_vks = set()
        self.combination_to_function = {
            frozenset([Key.ctrl_l, Key.shift]): screen_capture.capture_screen,  # shift + a
        }

    def get_vk(self, key):
        """
        Get the virtual key code from a key.
        These are used so case/shift modifications are ignored.
        """
        return key.vk if hasattr(key, 'vk') else key.value.vk

    def on_release(self, key):
        """ When a key is released """
        vk = self.get_vk(key)  # Get the key's vk
        if vk in self.pressed_vks:
            self.pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys

    def is_combination_pressed(self, combination):
        """ Check if a combination is satisfied using the keys pressed in pressed_vks """
        return all([self.get_vk(key) in self.pressed_vks for key in combination])

    def on_press(self, key):
        """ When a key is pressed """
        vk = self.get_vk(key)  # Get the key's vk
        self.pressed_vks.add(vk)  # Add it to the set of currently pressed keys

        for combination in self.combination_to_function:  # Loop through each combination
            if self.is_combination_pressed(combination):  # Check if all keys in the combination are pressed
                self.combination_to_function[combination]()  # If so, execute the function
                self.pressed_vks = set()
