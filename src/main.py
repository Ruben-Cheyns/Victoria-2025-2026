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


# vex device config
brain = Brain()
left_1 = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
left_2 = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
left_3 = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
left = MotorGroup(left_1, left_2, left_3)
right_1 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
right_2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
right_3 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
right = MotorGroup(right_1, right_2, right_3)
intake = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
gyro = Inertial(Ports.PORT17)
controller_1 = Controller()


# PID classes
class PID:
    "a beautiful well made pid system for all vex uses"

    def __init__(self ,yourSensor ,brain: Brain, KP: float = 1, KI: float = 0, KD: float = 0):
        self.KP = KP
        self.KI = KI
        self.KD = KD
        self.yourSensor = yourSensor
        self.brain = brain

    def run(self, desiredValue: int, tollerance: float):
        previousError = 0
        totalError = 0
        i = 0
        while abs(desiredValue - self.yourSensor) > tollerance:
            i += 1
            error = desiredValue - self.yourSensor
            derivative = error - previousError
            self.output = error * self.KP + derivative * self.KD + totalError * self.KI
            totalError += error
            wait(50)

    def tune(self, desiredValue: int, tollerance: float, sd_file_name = "pidData.csv"):
        csvHeaderText = "time, error, derivative, totalError, output, desiredValue"

        data_buffer = csvHeaderText + "\n"

        errorGraph = []
        derivativeGraph = []
        totalErrorGraph = []
        tGraph = []

        previousError = 0
        totalError = 0
        i = 0

        while abs(desiredValue - self.yourSensor) > tollerance:
            i += 1
            error = desiredValue - self.yourSensor
            derivative = error - previousError
            self.output = error * self.KP + derivative * self.KD + totalError * self.KI
            totalError += error
            wait(50)

            tGraph.append(i * 50)
            data_buffer += "%1.3f" % i * 50 + ","
            data_buffer += "%1.3f" % error + ","
            data_buffer += "%1.3f" % derivative + ","
            data_buffer += "%1.3f" % totalError + ","
            data_buffer += "%1.3f" % self.output + ","
            data_buffer += "%1.3f" % desiredValue + "\n"

            errorGraph.append(error)

            derivativeGraph.append(derivative)
            totalErrorGraph.append(totalError)
        self.brain.sdcard.savefile(sd_file_name, bytearray(data_buffer, 'utf-8'))

class turnPID(PID):
    
    def __init__(self, yourSensor, brain: Brain, leftMotorGroup: MotorGroup, rightMotorGroup: MotorGroup, KP: float = 1, KI: float = 0, KD: float = 0):
        self.KP = KP
        self.KI = KI
        self.KD = KD
        self.left = leftMotorGroup
        self.right = rightMotorGroup
        self.yourSensor = yourSensor
        self.brain = brain

    def run (self, desiredValue: int, tollerance: float):
        previousError = 0
        totalError = 0
        i = 0
        while abs(desiredValue - self.yourSensor) > tollerance:
            i += 1
            error = desiredValue - self.yourSensor
            derivative = error - previousError
            self.output = error * self.KP + derivative * self.KD + totalError * self.KI
            self.left.set_velocity(self.output, PERCENT)
            self.right.set_velocity(-self.output, PERCENT)
            totalError += error
            wait(50)

    def tune(self, desiredValue: int, tollerance: float, sd_file_name = "pidData.csv"):
        data_buffer: str = ""
        csvHeaderText = "time, error, derivative, totalError, output, desiredValue"

        data_buffer = csvHeaderText + "\n"

        previousError = 0
        totalError = 0
        i = 0

        while abs(desiredValue - self.yourSensor) > tollerance:
            i += 1
            error = desiredValue - self.yourSensor
            derivative = error - previousError
            self.output = error * self.KP + derivative * self.KD + totalError * self.KI
            self.left.set_velocity(self.output, PERCENT)
            self.right.set_velocity(-self.output, PERCENT)
            totalError += error
            wait(50)

            data_buffer += "%1.3f" %(i * 50) + ","
            data_buffer += "%1.3f" %(error) + ","
            data_buffer += "%1.3f" %(derivative) + ","
            data_buffer += "%1.3f" %(totalError) + ","
            data_buffer += "%1.3f" %(self.output) + ","
            data_buffer += "%1.3f" %(desiredValue) + "\n"

        self.brain.sdcard.savefile(sd_file_name, bytearray(data_buffer, 'utf-8'))

# PID setup    
rotateTune = turnPID(yourSensor= gyro, brain = brain ,leftMotorGroup=left, rightMotorGroup=right)
rotateTune.KP = 100
rotateTune.KI = 0
rotateTune.KD = 0

# autonomous 
def auton():
    # place automonous code here
    for i in range(0, 360, 30):
        right.spin(FORWARD, 0)
        left.spin(FORWARD, 0)
        #rotateTune.tune(i, 0.2, 'turnPID' + str(i) + '.csv') 
        rotateTune.tune(i, 0.2, f'turnPID.csv{i}°') 

# user control functions
def arcadeDrive(left: MotorGroup, right: MotorGroup, controller: Controller):
    """
    Arcade drive using the left joystick for forward/backward movement and the right joystick for turning.

    motorgroups: Left, Right
    controller: controller_1

    usecase:
        repeat in loop when driver control is active
    """
    left.set_velocity((controller.axis3.position() + controller.axis1.position()), PERCENT)
    right.set_velocity((controller.axis3.position() - controller.axis1.position()), PERCENT)
    left.spin(FORWARD)
    right.spin(FORWARD)

def intakeControl():
    """
    Controls the intake motor using the controller buttons.

    usecase:
        repeat in loop when driver control is active
    """
    if controller_1.buttonR1.pressing():
        intake.spin(FORWARD, 100, PERCENT)
    elif controller_1.buttonR2.pressing():
        intake.spin(REVERSE, 100, PERCENT)
    else:
        intake.stop(HOLD)

# user control 
def user_control():
    brain.screen.clear_screen()
    brain.screen.print("user control code")
    while True:
        arcadeDrive(left, right, controller_1)
        intakeControl()
        wait(20, MSEC)

# create competition instance
comp = Competition(user_control, auton)

# actions to do when the program starts
brain.screen.clear_screen()