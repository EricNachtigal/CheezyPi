# CheezyPi Version 0.1 Alpha
# 2023 Eric Nachtigal
# MIT License

import time
import os
import random
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

#Seeding randomness using os.urandom function
randseed = int.from_bytes(os.urandom(1), "big")
random.seed(randseed)

# Creating the keyboard object and needed variables
time.sleep(1)  # Sleep to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
key_space = Keycode.SPACE

print("Simulate pressing spacebar at a random interval between 2 and 5 mins")

''' Move to this format to help with webserver errors
try:
	your_application_here()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 10 seconds")
    time.sleep(10)
    microcontroller.reset()
'''

# Loop runs indefinately pressing spacebar every 2-5 mins with a randomly timed key
while 1:
    rdelay = random.randint(120, 300)
    rpress = random.uniform(0.01, 0.1)
    print(rdelay)
    keyboard.press(key_space)
    time.sleep(rpress)
    keyboard.release(key_space)  # ..."Release"!
    time.sleep(rdelay)
    print("Loop")
