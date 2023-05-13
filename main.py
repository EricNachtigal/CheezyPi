# CheezyPi Version 0.2.0
# 2023 Eric Nachtigal
# MIT License

import time
import os
import random
import microcontroller
import usb_hid
from adafruit_hid.keyboard import Keyboard # type: ignore
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS # type: ignore
from adafruit_hid.keycode import Keycode # type: ignore
import ipaddress
import wifi
import socketpool
from digitalio import DigitalInOut, Direction
from adafruit_httpserver.server import HTTPServer # type: ignore
from adafruit_httpserver.request import HTTPRequest # type: ignore
from adafruit_httpserver.response import HTTPResponse # type: ignore
from adafruit_httpserver.methods import HTTPMethod # type: ignore
from adafruit_httpserver.mime_type import MIMEType # type: ignore
import board # type: ignore

# logical status variables e.g. cheese_loop true activates the keypress loop
cheese_loop = True

# Onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

#Seeding randomness using os.urandom function
randseed = int.from_bytes(os.urandom(1), "big")
random.seed(randseed)

# Creating the HID objects and setting HID variables
time.sleep(1)  # Sleep to avoid a race condition on some systems
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
key_space = Keycode.SPACE

# Function to press and release the provided key
def keypress(target_key):
    print("Key Pressed!")
    rpress = random.uniform(0.01, 0.1)
    keyboard.press(target_key)
    time.sleep(rpress)
    keyboard.release(target_key)  # ..."Release"!

# Function to get Pico W CPU temp in C
def get_temp():
    temp = microcontroller.cpu.temperature # the cooler CPU is likely closest to ambient temp
    return temp

# Connect to wifi, print mac address, and ping google. Set Static IP variables in the .env file.
print("Sleep for 10 seconds")
time.sleep(10)
led.value = cheese_loop
try:
    print()
    print("Connecting to WiFi")
        
    #  set static IP address
    ipv4 =  ipaddress.IPv4Address(os.getenv('CIRCUITPY_STATIC_IP'))
    netmask =  ipaddress.IPv4Address(os.getenv('CIRCUITPY_NETMASK'))
    gateway =  ipaddress.IPv4Address(os.getenv('CIRCUITPY_GATEWAY'))
    wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
        
    #  connect to your SSID
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

    print("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    server = HTTPServer(pool, "/static")
    temp_test = get_temp()
    print("Temp Got")
    unit = "C"
    # HTML Font
    font_family = "monospace"

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

#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting
def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto; height: 50px;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Pico W HTTP Server</h1>
    <p class="dotted">This is a Pico W running an HTTP server with CircuitPython.</p>
    <p class="dotted">The current CPU temperature of the Pico W is 
    <span style="color: deeppink;">{temp_test}°{unit}</span></p>
    <p class="dotted">The keypress loop status is: 
    <span style="color: deeppink;">{cheese_loop}</span></p>
    <h1>Press selected key with the Pico W with this button:</h1>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="SPACEBAR" value="SPACEBAR" type="submit">Spacebar</button></a></p></form>
    <h1>Control the keypress loop on the Pico W with these buttons:</h1>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="KEYPRESS ON" value="ON" type="submit">KEYPRESS ON</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="KEYPRESS OFF" value="OFF" type="submit">KEYPRESS OFF</button></a></p></form>
    </body></html>
    """
    return html

#  route default static IP
@server.route("/")
def base(request: HTTPRequest):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

#  if a button is pressed on the site
@server.route("/", method=HTTPMethod.POST)
def buttonpress(request: HTTPRequest):
    global cheese_loop
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    # if the keypress on button was pressed
    if "ON" in raw_text:
        #  turn on keypress loop
        cheese_loop = True
    # if the keypress off button was pressed
    if "OFF" in raw_text:
        #  turn off the keypress loop
        cheese_loop = False
    if "SPACEBAR" in raw_text:
        #  Press Spacebar
        keypress(key_space)
    led.value = cheese_loop    
    with HTTPResponse(request, content_type=MIMEType.TYPE_HTML) as response:
        response.send(f"{webpage()}")

print("starting server..")
# startup the server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()
ping_address = ipaddress.ip_address("8.8.4.4")

report_clock = time.monotonic() # time.monotonic() holder for serial connection test and reporting
keypress_clock = time.monotonic() # time.monotonic() holder for the cheese loop
rdelay = random.randint(120, 300)
print("Current delay is %s s" % rdelay)

while True:
    try:
        #  every 30 seconds, ping server & update temp reading
        if (report_clock + 30) < time.monotonic():
            if wifi.radio.ping(ping_address) is None:
                print("lost connection")
            else:
                print("connected")
            report_clock = time.monotonic()
            temp_test = get_temp()
            print("Temperature: %s C" % temp_test)
            print("Keypress Loop: %s" % cheese_loop)
            if (keypress_clock + rdelay) < time.monotonic():
                print("Over delay, pending keypress when active")
            else:
                delay_countdown = int(keypress_clock) + rdelay - int(time.monotonic())
                print("Next press (if active) in %s s" % delay_countdown)
        # If this has jumped over a press this will press spacebar when 
        # the loop is set potential issues if using browser on host machine
        if cheese_loop and (keypress_clock + rdelay) < time.monotonic():
                keypress(key_space)
                keypress_clock = time.monotonic()
                rdelay = random.randint(120,300)
                print("Current delay is %s s" % rdelay)
        server.poll()
    # pylint: disable=broad-except
    except Exception as e:
        print(e)
        continue