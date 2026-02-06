#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Move Arc Joint
"""

import os
import sys
import time
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
# if len(sys.argv) >= 2:
#     ip = sys.argv[1]
# else:
#     try:
#         from configparser import ConfigParser
#         parser = ConfigParser()
#         parser.read('../robot.conf')
#         ip = parser.get('xArm', 'ip')
#     except:
#         ip = input('Please input the xArm ip address:')
#         if not ip:
#             print('input error, exit')
#             sys.exit(1)
########################################################


arm = XArmAPI('192.168.1.222')
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# arm.move_gohome(wait=True)

speed = 18

angles = [
    # [0, 14, -25, 0, 12.9, 0],
    [-14, 40, -75, 0, 33.4, -13.8],
    # [21.9, 50, -80, 50, 37, 29],
    # [0, 0, -156, 17, 32, 29]
]

test = [
    [-85, 18.481212, -2.15266, -359.999925, -0.000344, 180.000134],
    [-85, 18.481212, -2.15266, -359.999925, -31, 180.000134]
]

rest = [-15.241766, 18.481212, -2.15266, -359.999925, -0.000344, 180.000134]
# arm.set_pause_time(1)

for angle in test:
    code = arm.set_servo_angle(angle=angle, speed=speed, radius=60, wait=False)

# arm.set_servo_angle(servo_id=1, angle=-85, speed=speed, radius=60, wait=False)
# arm.set_servo_angle(servo_id=5, angle=-31, speed=speed, radius=60, wait=True)


# arm.set_servo_angle(angle=rest, speed=speed, radius=60, wait=False)

# print(arm.get_servo_angle(is_radian=False)[1][:-1])
# arm.move_gohome(wait=True)
arm.disconnect()