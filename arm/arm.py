import os
import sys
import time
import math
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI

# j1 = base rotation
# j2 = upper arm
# j3 = lower arm tilt
# j4 = lower arm rotation
# j5 = wrist tilt
# j6 = writs rotaion

class Arm:
    arm = XArmAPI('192.168.1.222')
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    # arm.move_gohome(wait=True)

    speed = 38

    rest = [-15.241766, 18.481212, -2.15266, -359.999925, -0.000344, 180.000134]

    def go_to_rest(self):
        # self.arm.set_servo_angle(angle=self.rest, speed=self.speed, radius=60, wait=True)
        self.arm.set_servo_angle(angle=[4.827581, -0.203028, 0.008842, 0.133888, -1.652684, 2.99643, 0.0], speed=20, is_radian=True, radius=60, wait=False)


    # def __del__(self):
    #     # self.go_to_rest()
    #     self.arm.set_state(state=4)
    #     self.arm.disconnect()

    def get_pos(self):
        # Returns a list containing [X,Y,Z,Roll,Pitch,Yaw]

        # self.arm.set_position(x=350, speed=self.speed)
        # pos = self.arm.get_position()[1]
        # print(pos)
        # pos[0] = 350 if round(pos[0]) !=350 else 487
        # angle = self.arm.get_servo_angle()
        # print(angle)
        # return self.arm.get_inverse_kinematics(pos)
        return self.arm.get_position()[1]
    
    def get_anlges(self):
        return self.arm.get_servo_angle(is_radian=True)[1]

    def set_pos(self):
        self.arm.set_position(164.788101, -132.823807, 333.87796, -11.789351, 75.391047, -57.866044)


















    def test_move_joint(self, joint=None, angle=None):
        curr = self.arm.get_servo_angle(is_radian=False)[1][:-1]
        print(curr)
        if joint is None:
            curr = [a_i + b_i for a_i, b_i in zip(curr, angle)]
        else:
            curr[joint-1] += angle

        print(curr)
        self.arm.set_servo_angle(angle=curr, speed=self.speed, radius=60, wait=True)

    def test(self):
        curr = arm.get_anlges()
        curr[0] += 7
        curr[3] += 7
        curr[5] -= 2
        self.arm.set_servo_angle(angle=curr, speed=10, radius=60, wait=False)


# arm.move_joint(2, -20)
if __name__ == "__main__":
    arm = Arm()
    # arm.
    # print(arm.get_anlges())
    # arm.set_pos()

    # for i in range(6):
    #     arm.test()
    # arm.get_anlges

    # arm.go_to_rest()
    arm.arm.set_servo_angle(angle=[-15.241766, 18.481212, -2.15266, -359.999925, -0.000344, 180.000134], speed=20, is_radian=False, radius=60, wait=False)

    

#[1.699168, 0.194476, -0.363007, -0.358848, -1.342569, 3.108848, 0.0] camera test pos
# -y is forwards
