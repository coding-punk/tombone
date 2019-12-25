# tombone
code for the tombstone clone robot.

The robot uses a tank drive with motors on the two side wheels.
The blade structure is supported by a single caster.

It is controlled over bluetooth using a ps3 controller. The two
sticks control the wheels while the left and right triggers control
the spinning of the blade (left trigger spins it clockwise, right
trigger spins it counter-clockwise).

The joystick has a response curve comprised of two separate functions
depending on the the input value:

y = .2x + 1.6x^3 + .5x^5 {|x| <= .65}

y = x {|x| > .65}

This allows for finer control at lower speeds while also providing linear
response at higher speeds. 

. 
