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
global current_state, counter, cone_queue, turn

rc = racecar_core.create_racecar()
counter = 0
cone_queue = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
turn = False
# Add any global variables here

class State(IntEnum):
    line_follow = 0
    line_follow_final = 1
    cone_follow = 2
    cone_park = 3
    cone_sweep = 4
    cone_initial_search = 5
    cone_search = 6


"""
This function is run once every time the start button is pressed
"""
def start():
    global current_state, last_color_seen
    # Have the car begin at a stop
    rc.drive.stop()
    current_state = State.cone_initial_search
    last_color_seen = None
    
    # Print start message
    print(">> Phase 1 Challenge: Cone Slaloming")

"""
After start() is run, this function is run every frame until the back button
is pressed
"""
def update():
    # TODO: Slalom between red and blue cones.  The car should pass to the right of
    # each red cone and the left of each blue cone.
    global counter
    speed, angle  = 0, 0
    if(current_state == State.cone_initial_search):
        speed, angle = initial_cone_search()
    elif(current_state == State.cone_search):
        counter = 0
        speed, angle = cone_search()
    elif(current_state == State.cone_sweep):
        speed, angle = cone_sweep()
    # else:
    #     speed, angle = 0, 0

    rc.drive.set_speed_angle(speed, angle)
    counter += rc.get_delta_time()

# angle turn time, straight time
def initial_cone_search():
    global counter, current_state
    countour_center, contour_area, side = find_cone()
    angle = 0
    if(contour_area < 0):
        if(counter < 7):
            angle = 0
        else:
            counter = 0
            current_state = State.cone_sweep
            return 0, 0

    if(counter < 3):
        angle = cone_queue[0] * 1
    else:
        angle = 0
    
    counter += rc.get_delta_time()

    return constants.CONE_SLALOM_SPEED, angle

def cone_search():
    global counter, current_state, cone_queue, turn
    countour_center, contour_area, side = find_cone()
    angle = 0

    if(contour_area < 0):
        if(counter < 1):
            angle = 0
        else:
            counter = 0
            current_state = State.cone_sweep
            return 0, 0
        counter += rc.get_delta_time()

    setpoint = 0
    offset = 183.5
    if(countour_center is not None and side == 1):
        setpoint = countour_center[1] + offset
    elif(countour_center is not None and side == -1):
        setpoint = countour_center[1] - offset

    angle = get_controller_output([3, 0, 0], setpoint, [-1, 1])
    print(angle)

    return constants.CONE_SLALOM_SPEED, angle

def cone_sweep():
    global counter, current_state, cone_queue
    angle = 0
    if(counter < 1.5):
        angle = -1 * cone_queue[0]
    else:
        current_state = State.cone_search
        cone_queue.pop(0)
        return 0, 0

    return constants.CONE_SLALOM_SPEED, angle


def find_cone():
    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, constants.CONE_SLALOM_IMG_CROP[0], constants.CONE_SLALOM_IMG_CROP[1])

    red_contour_center, red_contour_area = find_contours(constants.RED_CONE, cropped_image, True)
    blue_contour_center, blue_contour_area = find_contours(constants.BLUE_CONE, cropped_image, True)
    countour_center, contour_area = None, -1
    side = 0

    if red_contour_area > blue_contour_area:
        side = 1
        countour_center = red_contour_center
        contour_area = red_contour_area
    elif(blue_contour_area >= red_contour_area):
        side = -1
        countour_center = blue_contour_center
        contour_area = blue_contour_area

    return countour_center, contour_area, side


def find_contours(color, image, show):    
    # When the image is not found: None, None is returned
    if image is None:
        # print("No Image")
        return None, None
        
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])

    # Gets the largest contour
    contour = rc_utils.get_largest_contour(list_contours, constants.CONE_SLALOM_MIN_CONTOUR)

    # If no contour was found: None, None is returned
    if(contour is None):
        # print("No contour found")
        return None, -1

    # Gets information about the center and area
    contour_center = rc_utils.get_contour_center(contour)
    contour_area = rc_utils.get_contour_area(contour)

    if(show):
        rc_utils.draw_contour(image, contour)
        rc_utils.draw_circle(image, contour_center)
        
        rc.display.show_color_image(image)

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
