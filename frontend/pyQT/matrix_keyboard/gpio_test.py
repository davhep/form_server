#!/usr/bin/env python

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import RPi.GPIO as GPIO
import time

# Pin Definitions
input_pin = 37  # BCM pin 18, BOARD pin 12



def keypadCallback(channel):
    global keypadPressed
    print("aaa")
    print(str(channel)+" pressed" + str(keypadPressed))
    keypadPressed = keypadPressed + 1
    value = GPIO.input(input_pin)
    #if value != prev_value:
    if value == GPIO.HIGH:
        value_str = "HIGH"
    else:
        value_str = "LOW"
    print("Value read from pin {} : {}".format(channel,
                                               value_str))

def main():
    prev_value = None
    global keypadPressed
    keypadPressed = 0
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(35, GPIO.OUT)
    GPIO.output(35, GPIO.HIGH)
    GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin
    GPIO.add_event_detect(input_pin, GPIO.RISING, callback=keypadCallback, bouncetime=1000)
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            value = GPIO.input(input_pin)
            #if value != prev_value:
            if value == GPIO.HIGH:
                value_str = "HIGH"
            else:
                value_str = "LOW"
            print("Value read from pin {} : {}".format(input_pin,
                                                       value_str))
            prev_value = value
            time.sleep(0.25)

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
