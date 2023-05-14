# CheezyPi
Web Enabled HID AFK tool for the PicoW(Possibly any CircutPy device). Currently can be set to press spacebar via a local web UI. Using CircutPython 8.0.5

# Setup
Set your SSID and Static IP settings in the settings.toml file:  

CIRCUITPY_WIFI_SSID="YourSSIDHere"\
CIRCUITPY_WIFI_PASSWORD="YourPasswordHere"\
CIRCUITPY_STATIC_IP="XXX.XXX.XXX.XXX"\
CIRCUITPY_NETMASK="XXX.XXX.XXX.XXX"\
CIRCUITPY_GATEWAY="XXX.XXX.XXX.XXX"

# Use
The CheezyPi will take ~30 seconds to initilize. The green board LED will light up when everything is configured and indicate the status of the AFK loop. The webpage should be available at this time. Navigate to the static IP address you configured for the device and follow the on screen instructions.

# Help
If the webpage is not available after the status LED is up. Restart the device and open a serial monitor program such as Puttty to read the output. Alternatively you can restart the device while allready connected via opening and saving (making no changes) to the main.py file on the device itself.

# Roadmap
## HID Features
- [x] Press spacebar at a rand intervel when plugged in
- [ ] W/A, S/D 'balanced' combo presses
- [ ] Variable based programable time ranges for press and release as well as delay
- [ ] Mouse input emulation

## WebFeatures
- [x] Enable start/stop from webpage
- [ ] Report next keypress countdown to webpage
- [ ] Report number of anti-AFK actions this session to webpage
- [ ] Select actions to take from webpage 

## General Features
- [ ] Local enable/disable switch
- [x] Status LED