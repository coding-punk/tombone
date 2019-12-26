import logging
import os.path
import signal
import time
from logging import handlers

import pygame
from adafruit_servokit import ServoKit

LOG_FILENAME = "/var/log/tombone.log"
logger = logging.getLogger("coding-punk.tombone")
logger.setLevel(logging.DEBUG)

# keep 10 1MB log files
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=10)
logger.addHandler(handler)

kit = ServoKit(channels=16)

# the motors on the servo board
left_motor = kit.continuous_servo[1]
right_motor = kit.continuous_servo[2]
spinner = kit.continuous_servo[3]

# joystick axes
left_stick = 1
right_stick = 4
left_trigger = 2
right_trigger = 5

# map the axes to the motors
axis_dict = {
    left_stick: left_motor,
    right_stick: right_motor,
    left_trigger: spinner,
    right_trigger: spinner
}

# signal to terminate the loop
keep_running = True


# the main control loop
def loop():
    print("in the loop")
    while keep_running:
        # wait for joystick event
        for event in pygame.event.get():
            # this *should* always be true
            if event.type == pygame.JOYAXISMOTION:
                axis = event.dict['axis']
                if axis in [1,2,4,5]:
                    motor = axis_dict[axis]
                    value = event.dict['value']
                    # special handling for axis 5, invert its readings
                    # so it spins the spinner in reverse
                    if axis in [2,5]:
                        if value < 0:
                            value = 0
                    if axis in [1,5]:
                        value = value * -1
                    control_motor(motor, value)
    pygame.display.quit()
    pygame.quit()


# this calculates the joystick response curve
# if 1 > |x| > .67 it is linear, otherwise
# y = .2x + 1.6x^3 + .5x^5
def calculate_curve(raw_input):
    x = raw_input
    if x > 1:
        x = 1
    else:
        if x < -1:
            x = -1
    print("raw_input is {0} and x is {1}".format(raw_input, x))
    equation_cutoff = 0.67
    if abs(x) <= equation_cutoff:
        calc = (0.2 * x) + (1.6 * (x ** 3)) + (0.5 * (x ** 5))
        print('raw input: {0} output: {1}'.format(raw_input, calc))
        return calc
    else:
        print('raw input: {0} output: {0}'.format(raw_input))
        return x


# takes the raw reading of the joystick
# and tells the motor what to do
def control_motor(motor, reading):
    value = calculate_curve(reading)
    motor.throttle = value


def handle_signals():
    # register the signals to be caught, turns out the Pi can only handle these signals
    for sig in [signal.SIGILL, signal.SIGABRT, signal.SIGFPE, signal.SIGSEGV, signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, terminate_loop)


# allow the program to gracefully exit
def terminate_loop():
    global keep_running
    keep_running = False


def main():
    print("starting up")
    logger.info("starting tombone")
    # gracefully handle signals
    
    #handle_signals()
    print("setting up pygame")
    pygame.init()
    # we only want the pygame.JOYAXISMOTION events
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.JOYAXISMOTION)

    # need to init the display because the event queue relies on it
    print("setting up the display")
    pygame.display.init()

    # set up the joystick to get events
    print("waiting for joystick")
    while pygame.joystick.get_count() == 0:
        print("waiting for joystick count to go past {0}".format(pygame.joystick.get_count()))
        time.sleep(5)
        pass
    print("setting up joystick")
    joy = pygame.joystick.Joystick(0)
    joy.init()
    
    # start handling events
    print("calling loop")
    loop()
    logging.info("ending tombone")


if __name__ == "__main__":
    main()
