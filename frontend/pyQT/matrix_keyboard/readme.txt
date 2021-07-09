Working with matrix keyboard is based on gpio monitoring, see matrix_sample.py
Jetson Nano h/w requires pull-down resistors about 3.5 kOmh (1 kOmh too low, 6 kOmh too high).
With pull-down resistor betwee 39 (GND) and 37(INPUT) pins, basic gpio_test.py works well.
