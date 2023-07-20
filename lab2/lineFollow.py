# imports
import sys
from enum import IntEnum

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from nptyping import NDArray

sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

# global variables
global rc, color_queue_timer, color_queue_index, integral_sum, PID_timer, last_error
integral_sum = 0.0
PID_timer = 0.0
last_error = 0.0

rc = racecar_core.create_racecar()

# HSV Values
BLUE = ((90,70,70), (110,255,255))
RED = ((170,100,100), (10,255,255))
GREEN = ((40,50,50), (80,255,255))
ORANGE = ((0,254,254), (1,255,255))
YELLOW = ((10,50,50), (30,255,255))

WIDTH = 320
HEIGHT = 240

# color_queue:   holds tuples of the current color, + next,
#                will be incremented when next is found
color_queue = ((GREEN, ORANGE), (GREEN, ORANGE), (RED, BLUE), (BLUE, ORANGE))
color_queue_index = 0
color_queue_timer = 0

MIN_CONTOUR_AREA = 30
LINE_FOLLOW_IMG_CROP = ((100,0), (240, 320))
LINE_STRAIGHT_IMG_CROP = ((120,120), (180,200))


DEFAULT_SAFE_SPEED = 0.15
LINE_FOLLOWING_SPEED = 0.15
LINE_STRAIGHT_SPEED = 0.2

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
    global PID_timer
    PID_timer += rc.get_delta_time()
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
    if color_queue_timer <= 0 and next_contour_area > 1000:
        print("next found")
        # The color_queue_index index is incremented so that we can look for the next color pair
        color_queue_index += 1
        # The timer is set 1, cooldown timer so that the camera doesnt immediatley switch colors
        color_queue_timer = 2
        # The current values are set to the next values
        current_contour_center, current_contour_area = next_contour_center, next_contour_area

    # The angle is returned based off of the x value of the current contour center
    angle = get_controller_output(current_contour_center[1])

    # Decrements the color_queue_timer by the delta time so that we know when 1 second has passed
    if color_queue_timer > 0:
        color_queue_timer -= rc.get_delta_time()

    # Checks if car is on long straight-away, and returns faster speed
    long_contour_center, long_contour_area = findContoursLine(color_queue[color_queue_index][0], LINE_STRAIGHT_IMG_CROP)
    if long_contour_area > 1000:
        print("ZOOM")
        return LINE_STRAIGHT_SPEED, angle
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
        return None, 0
    
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
        return None, 0

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
    global integral_sum, last_error, PID_timer
    kP = 0.001
    kI = 0.00
    kD = 0.00
    #range center =  0 - 320
    #   error = -160 - +160
    #   output_rc = -1 - 1
    error = center - (WIDTH / 2)
    integral_sum += PID_timer * error
    slope = error - last_error / PID_timer    
    output_px = (kP * (error) + (kI * integral_sum) + (kD * slope))

    output_rc = output_px / (WIDTH / 2)
    last_error, PID_timer = error, 0
    return clamp(output_rc, -1, 1)

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

