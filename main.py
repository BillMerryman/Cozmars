import os
import time

from Cozmars_Motor_Control import motors
from Cozmars_Face_Control import face

def salute_up():
	motors.set_lift(80)
	motors.set_head(100)

def salute_down():
	motors.set_lift(20)
	motors.set_head(75)

def main():
	face_animate = face.FaceAnimate()
	face_animate.start()
	time.sleep(1)
	salute_up()
	salute_down()
	motors.rotate_right(180)
	time.sleep(2.2)
	motors.rotate_left(180)
	time.sleep(2)
	motors.move_forward(0)
	face_animate.set_face("GraphicDev/sarge_eye_squint_transparent.png")
	os.system('padsp /opt/swift/bin/swift "Listen up soldier, you can bite my rusty metal az. You aren\'t ready for this robots army."')
	face_animate.set_face("GraphicDev/sarge_eye_transparent.png")
	face_animate.stop()
	face_animate.join()

if __name__ == "__main__":
    main()

