# CheezyPi Version 0.1 Alpha
# 2023 Eric Nachtigal
# MIT License

import time
import os
import random
import microcontroller
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import ipaddress
import wifi
import socketpool
from digitalio import DigitalInOut, Direction
import adafruit_httpserver
import board # type: ignore

#  onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

#Connect to wifi, print mac address, and ping google.
def wifi_test():
    try:
        print()
        print("Connecting to WiFi")

        #  connect to your SSID
        wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

        print("Connected to WiFi")

        pool = socketpool.SocketPool(wifi.radio)

        #  prints MAC address to REPL
        print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

        #  prints IP address to REPL
        print("My IP address is", wifi.radio.ipv4_address)

        #  pings Google
        ipv4 = ipaddress.ip_address("8.8.4.4")
        print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
    except Exception as e:
        print("Error:\n", str(e))
        print("Resetting microcontroller in 10 seconds")
        time.sleep(10)
        microcontroller.reset()

wifi_test() 

#Seeding randomness using os.urandom function
randseed = int.from_bytes(os.urandom(1), "big")
random.seed(randseed)

# Creating the keyboard object and needed variables
time.sleep(1)  # Sleep to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
key_space = Keycode.SPACE

print("Simulate pressing spacebar at a random interval between 2 and 5 mins")

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

''' Move to this format to help with webserver errors
try:
	your_application_here()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 10 seconds")
    time.sleep(10)
    microcontroller.reset()
'''
 