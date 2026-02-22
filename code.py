import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Setup keyboard
kbd = Keyboard(usb_hid.devices)

# Assign GPIO pins to switches
switch_pins = {
    board.GP11: Keycode.W,
    board.GP12: Keycode.A,
    board.GP13: Keycode.S,
    board.GP14: Keycode.D,
    board.GP15: Keycode.LEFT_CONTROL
}

# Setup switches as digital inputs with pull-down resistors
switches = {}
for pin, key in switch_pins.items():
    switch = digitalio.DigitalInOut(pin)
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.DOWN
    switches[switch] = key

# Track switch states to avoid repeat key presses
pressed_states = {pin: False for pin in switches}

while True:
    for pin, key in switches.items():
        if pin.value and not pressed_states[pin]:
            kbd.press(key)
            pressed_states[pin] = True
        elif not pin.value and pressed_states[pin]:
            kbd.release(key)
            pressed_states[pin] = False