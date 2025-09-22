from vex import *

# ---------------------------------------------------------------------------- #


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
    
def changeDriveGraph(controller: Controller):
    """
    changes the constant in the DriveGraph on button press
    """
    global k
    if controller.buttonUp.pressed:
        k+=1
    elif controller.buttonDown.pressed:
        k-=1
    controller.screen.clear_screen()
    controller.screen.print(k)

def driveGraph(x):
    """
    a simple mathemathic function to translate controller input into velocity output
    """
    if x > 0:
        return (x**k)/10**((k-1)*2)
    else:
        return -(x**k)/10**((k-1)*2)

def arcadeDriveGraph(left: MotorGroup, right: MotorGroup, controller: Controller):
    """
    Arcade drive using the left joystick for forward/backward movement and the right joystick for turning.
    a graph translates forward controller input to forward speed

    motorgroups: Left, Right
    controller: controller_1

    usecase:
        repeat in loop when driver control is active
    """
    left.set_velocity((driveGraph(controller.axis3.position()) + controller.axis1.position()), PERCENT)
    right.set_velocity((driveGraph(controller.axis3.position()) - controller.axis1.position()), PERCENT)
    left.spin(FORWARD)
    right.spin(FORWARD)