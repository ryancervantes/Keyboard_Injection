"""
Author: Ryan Cervantes (rxc3202@rit.edu)
Date: 11/6/2019
"""
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import adafruit_hid.keyboard_layout_us as layout
import time

RUN = False

special_chars = {
    "<TAB>" : Keycode.TAB,
    "<ENTER>" : Keycode.ENTER,
    "<SPACE>" : Keycode.SPACE,
    "<SHIFT>" : Keycode.SHIFT,
    "<ALT>" : Keycode.ALT,
    "<CTRL>" : Keycode.CONTROL,
    "<DEL>" : Keycode.DELETE,
    "<ESC>" : Keycode.ESCAPE
}

mouse_click = {
    "LEFT": Mouse.LEFT_BUTTON,
    "MIDDLE": Mouse.MIDDLE_BUTTON,
    "RIGHT": Mouse.RIGHT_BUTTON
}

if RUN:
    # Init HID Keyboard
    kbd = Keyboard()
    mouse = Mouse()
    USLayout = layout.KeyboardLayoutUS(kbd)

    OS = "WINDOWS"
    PROGRAM = ""
    STEPS = []

    # Read in Commands from commands file
    with open('/steps.txt') as commands:
        for line in commands:
            line = line.strip("\n\r ")
            if '#' in line:
                continue

            if "PROGRAM" in line:
                line = line.split("=")
                PROGRAM = line[1].strip()
                continue

            if "OS" in line:
                line = line.split("=")
                OS = line[1].strip().upper()
                print(OS)
                continue

            if not line == '':
                STEPS.append(line)
    commands.close()

    # Open program
    if PROGRAM != "NONE":
        time.sleep(.5)
        search_keycodes = (Keycode.WINDOWS,) if OS == "WINDOWS" else (Keycode.COMMAND, Keycode.SPACE)
        kbd.send(*search_keycodes)
        time.sleep(.5)
        USLayout.write(PROGRAM)
        time.sleep(.25)
        kbd.send(Keycode.ENTER)
        time.sleep(2)

    for step in STEPS:
        if "KEYS" in step:
            codes = tuple(special_chars[code]
            for code in step.split("KEYS")[1].strip().split(' '))
            kbd.send(*codes)
        elif "WAIT" in step:
            sec = step.split(" ")[1]
            time.sleep(float(sec))
        elif "MOUSE" in step:
            x,y = step.split(" ")[1:]
            mouse.move(int(x), int(y))
        elif "CLICK" in step:
            button = step.split(" ")[1].strip()
            mouse.click(mouse_click[button])
        else:
            USLayout.write(step)
            kbd.send(Keycode.ENTER)
        print(step)