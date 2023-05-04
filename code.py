# CheezyPi Version 0.1 Alpha
# 2023 Eric Nachtigal
# MIT License

import time
import random
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

#Seeding Universal Randomness (Maybe use temp sensor LSDs)
random.seed(42)

# Setting Keycodes as variables
key_space = Keycode.SPACE

# Creating the keyboard object
time.sleep(1)  # Sleep to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# Loop runs indefinately pressing spacebar every 2-5 mins with a randomly timed key
while true:
    rdelay = random.randint(120, 300)
    rpress = random.uniform(0.01, 0.1)
    keyboard.press(key_space)
    time.sleep(rpress)
    keyboard.release(key_space)  # ..."Release"!
    time.sleep(rdelay)
    print("Loop")
