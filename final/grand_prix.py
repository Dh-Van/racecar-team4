"""
Copyright MIT and Harvey Mudd College
MIT License
Fall 2020

Final Challenge - Grand Prix
"""
# Imports
import sys, cv2 as cv
import numpy as np
import scipy
import line_following, constants

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

# Global variables
color_queue = (
    (constants.BLUE_LINE, constants.GREEN_LINE), 
    (constants.GREEN_LINE, constants.RED_LINE), 
    (constants.RED_LINE, constants.BLUE_LINE),
    (constants.BLUE_LINE, constants.ORANGE_LINE)
)
rc = racecar_core.create_racecar()
lf = line_following.line_follow(rc, color_queue)

"""
This function is run once every time the start button is pressed
"""
def start():
    # Have the car begin at a stop
    rc.drive.stop()

    # Print start message
    print(">> Final Challenge - Grand Prix")

    # Feature Initialization
    lf.start()

"""
After start() is run, this function is run every frame until the back button
is pressed
"""
def update():
    # Feature Updates
    lf.update()
    # vc.set_velocity_angle(0.8, 0)
"""
DO NOT MODIFY: Register start and update and begin execution
"""
if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
