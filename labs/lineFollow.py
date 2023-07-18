# imports
import sys
from enum import IntEnum

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from nptyping import NDArray

sys.path.insert(1, "../library")
import racecar_core
import racecar_utils as rc_utils

# global variables
global rc, color_queue_timer, color_queue_index

rc = racecar_core.create_racecar()

# HSV Values
BLUE = ((90,50,50), (110,255,255))
RED = ((170,100,100), (10,255,255))
GREEN = ((50,50,50), (80,255,255))
ORANGE = ((0,254,254), (1,255,255))

# color_queue:   holds tuples of the current color, + next,
#                will be incremented when next is found
color_queue = ((BLUE, GREEN), (GREEN, RED), (RED, BLUE), (BLUE, ORANGE))
color_queue_index = 0
color_queue_timer = 0

MIN_CONTOUR_AREA = 30
LINE_FOLLOW_IMG_CROP = ((360,0), (480, 640))


DEFAULT_SAFE_SPEED = 0.15
LINE_FOLLOWING_SPEED = 1.0

# States class:
class State(IntEnum):
    line_follow = 0
    depth_camera_search = 1
    cone_park = 2

# Initialize current_state
curr_state = State.line_follow

# run-functions
def start():
    rc.drive.set_speed_angle(0, 0)

def update():
    # State Machine
    if(curr_state == State.line_follow):
        speed, angle = line_follow()
    elif(curr_state == State.depth_camera_search):
        pass
    elif(curr_state == State.cone_park):
        pass
    else:
        speed, angle = 0, 0

    rc.drive.set_speed_angle(speed, angle)

"""
Function for following a line based on the color queue.
This function returns a speed and angle value
"""
def line_follow():
    global color_queue_index, color_queue_timer
    # Initial speed and angle values will be set to safe value
    speed, angle = DEFAULT_SAFE_SPEED, 0

    # Gets info about the current color contour and the next color contour in the color queue
    current_contour_center, current_contour_area = findContoursLine(color_queue[color_queue_index][0], LINE_FOLLOW_IMG_CROP)
    next_contour_center, next_contour_area = findContoursLine(color_queue[color_queue_index][1], LINE_FOLLOW_IMG_CROP)

    # Returns the safe values when the current contour is none
    if(current_contour_center is None):
        return speed, angle

    # If the timer is not 1 and the next contour is found
    if color_queue_timer <= 0 and next_contour_center is not None:
        print("next found")
        # The color_queue_index index is incremented so that we can look for the next color pair
        color_queue_index += 1
        # The timer is set 1, cooldown timer so that the camera doesnt immediatley switch colors
        color_queue_timer = 1
        # The current values are set to the next values
        current_contour_center, current_contour_area = next_contour_center, next_contour_area

    # The angle is returned based off of the x value of the current contour center
    angle = get_controller_output(current_contour_center[1])

    # Decrements the color_queue_timer by the delta time so that we know when 1 second has passed
    if color_queue_timer > 0:
        color_queue_timer -= rc.get_delta_time()

    # The speed is a constant set above, and the angle is returned from the controller
    return LINE_FOLLOWING_SPEED, angle

'''
Function to get information about a contour based off a color
Requires a color (hsv tuple list), and a crop rectangle (list of x, y pairs)
Returns the largest contour center and area
'''
def findContoursLine(color, crop):
    image = rc.camera.get_color_image()
    
    # When the image is not found: None, None is returned
    if image is None:
        print("No Image")
        return None, None
    
    # Crop based off of the crop list
    image = rc_utils.crop(image, crop[0], crop[1])
    
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])


    # Gets the largest contour
    lg_contour = rc_utils.get_largest_contour(list_contours, MIN_CONTOUR_AREA)
 
    # cv.drawContours(image, [lg_contour], 0, (0,255,0), 3)
    # plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    # plt.show()

    # If no contour was found: None, None is returned
    if(lg_contour is None):
        return None, None

    # Gets information about the center and area
    contour_center = rc_utils.get_contour_center(lg_contour)
    contour_area = rc_utils.get_contour_area(lg_contour)

    # Returns the largest contour center and area
    return contour_center, contour_area

'''
takes in desired contour center x-value (in pixels),
and outputs new turn angle to correct error
'''
def get_controller_output(center):
    kP = 7
    return clamp(kP * (((center * (2 / 680))) - 1), -1, 1)

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
#Clamps the input

def show_image(image: NDArray) -> None:
    """
    Displays a color image in the Jupyter Notebook.
    """
    img = rc.camera.get_color_image()
    plt.show(img)
    
# DO NOT MODIFY: Register start and update and begin execution
if __name__ == "__main__":
    rc.set_start_update(start, update)
    rc.go()

