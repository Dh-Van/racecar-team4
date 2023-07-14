"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Lab 1 - Driving in Shapes
"""
global counter
counter = 0


########################################################################################
# Imports
########################################################################################

import sys

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################




rc = racecar_core.create_racecar()

# Put any global variables here

global queue
queue = [][]


########################################################################################
# Functions
########################################################################################


def start():
    """
    This function is run once every time the start button is pressed
    """
    # Begin at a full stop
    rc.drive.stop()

    # Print start message
    # TODO (main challenge): add a line explaining what the Y button does
    print(
        ">> Lab 1 - Driving in Shapes\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    A button = drive in a circle\n"
        "    B button = drive in a square\n"
        "    X button = drive in a figure eight\n"
    )


def update():
    global counter
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    # TODO (warmup): Implement acceleration and steering
    
    # rc.drive.set_speed_angle(-1, -1)

    if rc.controller.was_pressed(rc.controller.Button.A):
        print("Driving in a circle...")
        # TODO (main challenge): Drive in a circle
        rc.drive.set_speed_angle(1, 1)


    # TODO (main challenge): Drive in a square when the B button is pressed
    if rc.controller.is_(rc.controller.Button.B):
        print("Driving in a square...")
        counter = 0
        rc.drive.set_speed_angle(1, 0)
    
    if counter > 10:
        rc.drive.stop()

            
                    
            
    # TODO (main challenge): Drive in a figure eight when the X button is pressed
    if rc.controller.is_down(rc.controller.Button.X):
        print("Driving in a figure eight...")
        # TODO (main challenge): Drive in a circle
        rc.drive.set_speed_angle(-1, -1)
    # TODO (main challenge): Drive in a shape of your choice when the Y button
    # is pressed

    counter += rc.get_delta_time()


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()
