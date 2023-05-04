# SPDX-FileCopyrightText: 2023 Eric Nachtigal
#
# SPDX-License-Identifier: MIT

import time
import random
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

random.seed(42)
run = 1

# The Keycode sent for each button, will be paired with a control key
key_space = Keycode.SPACE

# The keyboard object!
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

print("Pressing Spacebar at a Random intervel between 2 and 5 mins")

while run:
    rdelay = random.randint(120, 300)
    rpress = random.uniform(0.01, 0.1)
    print(rdelay)
    print(rpress)
    #print("Pressing Space") #This Line is for Testing Purposes
    keyboard.press(key_space)
    time.sleep(rpress)
    keyboard.release(key_space)  # ..."Release"!
    time.sleep(rdelay)
    print("Bottom of Loop")
