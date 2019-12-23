import pygame
from adafruit_servokit import ServoKit

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

# raw joystick values are
max_joy_value = 37775

# signal to terminate the loop
keep_running = True


# the main control loop
def loop():
    while keep_running:
        # wait for joystick event
        for event in pygame.event.get():
            # this *should* always be true
            if event.type == pygame.JOYAXISMOTION:
                axis = event.dict['axis']
                motor = axis_dict[axis]
                value = event.dict['value']
                # special handling for axis 5, invert its readings
                # so it spins the spinner in reverse
                if axis == 5:
                    value = value * -1
                control_motor(motor, value)
    pygame.display.quit()
    pygame.quit()


# this calculates the joystick response curve
# if 1 > |x| > .67 it is linear, otherwise
# y = .2x + 1.6x^3 + .5x^5
def calculate_curve(raw_input):
    x = raw_input / max_joy_value
    equation_cutoff = 0.67
    if abs(x) <= equation_cutoff:
        return (0.2 * x) + (1.6 * x ^ 3) + (0.5 * x ^ 5)
    else:
        return input


# takes the raw reading of the joystick
# and tells the motor what to do
def control_motor(motor, reading):
    value = calculate_curve(reading)
    motor.throttle = value


def main():
    # we only want the pygame.JOYAXISMOTION events
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.JOYAXISMOTION)

    # need to init the display because
    # the event queue relies on it
    pygame.display.init()

    # set up the joystick to get events
    pygame.joystick.init()
    pygame.joystick.Joystick(0)

    # start handling events
    loop()


if __name__ == "__main__":
    main()