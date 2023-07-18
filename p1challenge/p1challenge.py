"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Phase 1 Challenge - Cone Slaloming
"""

# Imports

from enum import IntEnum
import sys
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import constants

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

# Global variables
global current_state

rc = racecar_core.create_racecar()


# Add any global variables here

class State(IntEnum):
    line_follow = 0
    line_follow_final = 1
    cone_slalom = 2
    cone_follow = 3
    cone_park = 4

"""
This function is run once every time the start button is pressed
"""
def start():
    global current_state
    # Have the car begin at a stop
    rc.drive.stop()
    current_state = State.cone_slalom
    
    # Print start message
    print(">> Phase 1 Challenge: Cone Slaloming")

"""
After start() is run, this function is run every frame until the back button
is pressed
"""
def update():
    # TODO: Slalom between red and blue cones.  The car should pass to the right of
    # each red cone and the left of each blue cone.
    speed, angle  = 0, 0
    multipler = 1
    if(current_state == State.cone_slalom):
        speed, angle = cone_slalom()
    else:
        speed, angle = 0, 0

    rc.drive.set_speed_angle(speed, angle)

def cone_slalom():
    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, constants.CONE_SLALOM_IMG_CROP[0], constants.CONE_SLALOM_IMG_CROP[1])

    contour_center, contour_area = find_contours(constants.RED_CONE, cropped_image, False)
    if(contour_area == None or contour_area == None):
        contour_center, contour_area = find_contours(constants.BLUE_CONE, cropped_image, False)
        multiplier = -1

    angle = get_controller_output(constants.CONE_SLALOM_GAINS, multiplier * (contour_center[1] + constants.DIST_ARC_TO_CONE_PX), (-1, 1))

    if(contour_area >= 5500):
        angle = 0

    return constants.CONE_SLALOM_SPEED, angle
    
    
def find_contours(color, image, show):    
    # When the image is not found: None, None is returned
    if image is None:
        print("No Image")
        return None, None
        
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])

    # Gets the largest contour
    contour = rc_utils.get_largest_contour(list_contours, constants.CONE_SLALOM_MIN_CONTOUR)

    # If no contour was found: None, None is returned
    if(contour is None):
        return None, None

    # Gets information about the center and area
    contour_center = rc_utils.get_contour_center(contour)
    contour_area = rc_utils.get_contour_area(contour)

    if(show):
        rc_utils.draw_contour(image, contour)
        rc_utils.draw_circle(image, contour_center)
        
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        plt.show()

    # Returns the largest contour center and area
    return contour_center, contour_area

def get_controller_output(gains, setpoint, clmp):
    return clamp(gains[0] * (((setpoint * (2 / rc.camera.get_width()))) - 1), clmp[0], clmp[1])

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

# DO NOT MODIFY: Register start and update and begin execution

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
