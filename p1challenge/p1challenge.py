"""
Copyright MIT and Harvey Mudd College
MIT License
Summer 2020

Phase 1 Challenge - Cone Slaloming
"""

# Imports
#region
from enum import IntEnum
import sys
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import constants
sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
#endregion

# Global variables
global current_state, last_state, slalom_timer

rc = racecar_core.create_racecar()

class States(IntEnum):
    Blue = -1
    Red = 1
    Turn = 2


"""
This function is run once every time the start button is pressed
"""
def start():
    global current_state, last_state, slalom_timer
    rc.drive.stop()

    current_state = States.Red
    last_state = None
    slalom_timer = 0

    # Print start message
    print(">> Phase 1 Challenge: Cone Slaloming")

"""
After start() is run, this function is run every frame until the back button
is pressed
"""
def update():
    # TODO: Slalom between red and blue cones.  The car should pass to the right of
    # each red cone and the left of each blue cone.
    global slalom_timer
    speed, angle  = 0, 0
    if(current_state == States.Blue):
        speed, angle = cone_search(States.Blue, constants.CS_BLUE_CONE_OFFSET, constants.BLUE_CONE)
    elif(current_state == States.Turn):
        speed, angle = turn()
    elif(current_state == States.Red):
        speed, angle = cone_search(States.Red, constants.CS_RED_CONE_OFFSET, constants.RED_CONE)

    slalom_timer += rc.get_delta_time()
    rc.drive.set_speed_angle(speed, angle)

def cone_search(state, offset, color):
    global current_state, last_state, slalom_timer

    # Gets contour center and area from the image
    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, constants.CS_IMG_CROP[0], constants.CS_IMG_CROP[1])
    contour_center, contour_area = find_contours(color, cropped_image, False)

    # Goes straight at the cone center + offset for 2.5 seconds
    if(slalom_timer <= constants.CS_STRAIGHT and contour_center is not None):
        angle_px = contour_center[1] + offset
        angle_rc = angle_px * (2 / 360) - 1
        return constants.CS_SPEED, clamp(angle_rc, -1, 1)

    # If it can still see the cone and 2.5 seconds is up, is keeps going straight
    if(contour_area >= 0):
        return constants.CS_SPEED, 0
    
    # If it can't see the cone and 2.5 seconds is up then it switches to the turn state
    # Sets timer to 0 so that hte same timer can be used for the turn() function
    slalom_timer = 0
    last_state = state
    current_state = States.Turn
    # Have to return 0,0 since the state machine requires a value. The state will only be switched next frame
    return 0, 0

def turn():
    global current_state, last_state, slalom_timer
    # Gets the contour area, center and the next state from the find_cone() function
    # next state lets us set the next state machine set at the end of this funciton depending on
    # the color of the biggest contour seen. Lets us keep going even if there are 2 cones of the same
    # color in a line
    contour_center, contour_area, next_state = find_cone()
    # Sets the angle to be negative of the last state value. The last_state int value is representative
    # of the side it should turn, so the negative value will let us turn around the cone
    angle = -last_state

    # First goes straight for 1.5 seconds. This is to account for the cone width. Since the fuction is called
    # right after the cone is not able to be seen, this lets us make sure that we won't hit the cone when we turn
    if(slalom_timer < 1.5):
        return constants.CS_SPEED, 0
    
    # Once 
    if((contour_area == -1 or contour_center == None) or slalom_timer < constants.CS_TURN):
        return constants.CS_SPEED, angle

    slalom_timer = 0
    last_state = States.Turn
    current_state = next_state
    return 0, 0
    

def find_cone():
    image = rc.camera.get_color_image()
    cropped_image = rc_utils.crop(image, constants.CS_IMG_CROP[0], constants.CS_IMG_CROP[1])

    red_contour_center, red_contour_area = find_contours(constants.RED_CONE, cropped_image, True)
    blue_contour_center, blue_contour_area = find_contours(constants.BLUE_CONE, cropped_image, True)
    countour_center, contour_area, state = None, -1, States.Turn

    if red_contour_area > blue_contour_area:
        countour_center = red_contour_center
        contour_area = red_contour_area
        state = States.Red
    elif(blue_contour_area >= red_contour_area):
        countour_center = blue_contour_center
        contour_area = blue_contour_area
        state = States.Blue

    return countour_center, contour_area, state


def find_contours(color, image, show):    
    # When the image is not found: None, None is returned
    if image is None:
        # print("No Image")
        return None, None
        
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])

    # Gets the largest contour
    contour = rc_utils.get_largest_contour(list_contours, constants.CS_MIN_CONTOUR)

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

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

# DO NOT MODIFY: Register start and update and begin execution

if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
