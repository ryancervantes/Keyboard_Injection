from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_hid.keyboard_layout_us as layout
import time
import os

RUN = True

special_chars = {
    "<TAB>" : Keycode.TAB,
    "<ENTER>" : Keycode.ENTER,
    "<SPACE>" : Keycode.SPACE
}

if RUN:
    # Init HID Keyboard
    kbd = Keyboard()
    USLayout = layout.KeyboardLayoutUS(kbd)

    PROGRAM = ""
    INTERVAL = 2
    STEPS = []

    # Read in Commands from commands file
    with open('/steps.txt') as commands:
        for line in commands:
            line = line.strip()
            if '#' in line:
                continue

            if "PROGRAM" in line:
                line = line.split("=")
                PROGRAM = line[1].strip(" ")
                continue

            line = line.strip("\n")
            if not line == '':
                STEPS.append(line)
    commands.close()

    # Open program
    time.sleep(.5)
    kbd.send(Keycode.WINDOWS)
    time.sleep(.5)
    USLayout.write(PROGRAM + "\n")
    time.sleep(2)

    for step in STEPS:
        if step in special_chars:
            kbd.send(special_chars[step])
        elif "WAIT" in step:
            sec = step.split(" ")[1]
            time.sleep(int(sec))
        else:
            USLayout.write(step)
            kbd.send(Keycode.ENTER)
        print(step)

