# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       RubenCheyns                                                  #
# 	Created:      4/28/2025, 1:04:28 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
from UserControl import *
from Autonomous import *

# vex device config
brain = Brain()
left_1 = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
left_2 = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
left_3 = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
left = MotorGroup(left_1, left_2, left_3)
right_1 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
right_3 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
right = MotorGroup(right_1, right_2, right_3)
gyro = Inertial(Ports.PORT17)
controller_1 = Controller()

# create competition instance
comp = Competition(user_control, auton)

# actions to do when the program starts
brain.screen.clear_screen()