import asyncio, time
from adafruit_servokit import ServoKit

LEFT_REVERSE = 4
LEFT_FORWARD = 5
RIGHT_REVERSE = 6
RIGHT_FORWARD = 7

HEAD = 8
LEFT_ARM = 9
RIGHT_ARM = 10

HEAD_MAX_POSITION = 100
HEAD_MIN_POSITION = 50
HEAD_REST_POSITION = 75
LIFT_MAX_POSITION = 80
LIFT_MIN_POSITION = 25

HEAD_START_POSITION = HEAD_REST_POSITION
LIFT_START_POSITION = LIFT_MIN_POSITION

HEAD_LAST_POSITION = HEAD_START_POSITION
HEAD_DELAY = .005
LIFT_LAST_POSITION = LIFT_START_POSITION
LIFT_OFFSET = 180
LIFT_DELAY = .005

kit = ServoKit(channels=16)
kit.servo[LEFT_REVERSE].set_pulse_width_range(0, 4000)
kit.servo[LEFT_FORWARD].set_pulse_width_range(0, 4000)
kit.servo[RIGHT_REVERSE].set_pulse_width_range(0, 4000)
kit.servo[RIGHT_FORWARD].set_pulse_width_range(0, 4000)

kit.servo[HEAD].angle = HEAD_LAST_POSITION
kit.servo[LEFT_ARM].angle = LIFT_OFFSET - LIFT_LAST_POSITION
kit.servo[RIGHT_ARM].angle = LIFT_LAST_POSITION
kit.servo[HEAD].angle = None
kit.servo[LEFT_ARM].angle = None
kit.servo[RIGHT_ARM].angle = None

def move_forward(speed_as_angle):
	kit.servo[LEFT_REVERSE].angle=0
	kit.servo[RIGHT_REVERSE].angle=0
	kit.servo[LEFT_FORWARD].angle=speed_as_angle
	kit.servo[RIGHT_FORWARD].angle=speed_as_angle


def move_reverse(speed_as_angle):
	kit.servo[LEFT_FORWARD].angle=0
	kit.servo[RIGHT_FORWARD].angle=0
	kit.servo[LEFT_REVERSE].angle=speed_as_angle
	kit.servo[RIGHT_REVERSE].angle=speed_as_angle
	
def rotate_left(speed_as_angle):
	kit.servo[LEFT_FORWARD].angle=0
	kit.servo[RIGHT_REVERSE].angle=0
	kit.servo[LEFT_REVERSE].angle=speed_as_angle
	kit.servo[RIGHT_FORWARD].angle=speed_as_angle
	
	
def rotate_right(speed_as_angle):
	kit.servo[LEFT_REVERSE].angle=0
	kit.servo[RIGHT_FORWARD].angle=0
	kit.servo[LEFT_FORWARD].angle=speed_as_angle
	kit.servo[RIGHT_REVERSE].angle=speed_as_angle
	
def set_head(angle):
	global HEAD_LAST_POSITION
	global HEAD_DELAY
	kit.servo[HEAD].angle = HEAD_LAST_POSITION
	if (angle - HEAD_LAST_POSITION) == 0:
		return
	degrees = abs(angle - HEAD_LAST_POSITION)
	increment = (angle - HEAD_LAST_POSITION) // abs(angle - HEAD_LAST_POSITION)
	for _ in range(degrees):
		HEAD_LAST_POSITION += increment
		kit.servo[HEAD].angle = HEAD_LAST_POSITION
		time.sleep(HEAD_DELAY)
	kit.servo[HEAD].angle = None
	
def set_lift(angle):
	global LIFT_LAST_POSITION
	global LIFT_OFFSET
	global LIFT_DELAY
	kit.servo[LEFT_ARM].angle = LIFT_LAST_POSITION
	kit.servo[RIGHT_ARM].angle = LIFT_OFFSET - LIFT_LAST_POSITION
	if (angle - LIFT_LAST_POSITION) == 0:
		kit.servo[RIGHT_ARM].angle = None
		kit.servo[LEFT_ARM].angle = None
		return	
	degrees = abs(angle - LIFT_LAST_POSITION)
	increment = (angle - LIFT_LAST_POSITION) // abs(angle - LIFT_LAST_POSITION)
	for _ in range(degrees):
		LIFT_LAST_POSITION += increment
		kit.servo[RIGHT_ARM].angle = LIFT_LAST_POSITION
		kit.servo[LEFT_ARM].angle = LIFT_OFFSET - LIFT_LAST_POSITION
		print("LEFT_ARM: " + str(kit.servo[LEFT_ARM].angle))
		print("RIGHT_ARM: " + str(kit.servo[RIGHT_ARM].angle))
		print("LIFT_LAST_POSITION: " + str(LIFT_LAST_POSITION))
		time.sleep(LIFT_DELAY)
	kit.servo[LEFT_ARM].angle = None
	kit.servo[RIGHT_ARM].angle = None

