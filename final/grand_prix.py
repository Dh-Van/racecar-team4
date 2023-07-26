"""
Copyright MIT and Harvey Mudd College
MIT License
Fall 2020

Final Challenge - Grand Prix
"""
# Imports
import sys
from line_following import line_follow
from states import States
import constants

sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils

# Global variables
color_queue = (
    (constants.BLUE_LINE, constants.GREEN_LINE), 
    (constants.GREEN_LINE, constants.RED_LINE), 
    (constants.RED_LINE, constants.BLUE_LINE),
    (constants.BLUE_LINE, constants.BLUE_LINE),
    (constants.HSV_NOTHING, constants.HSV_NOTHING)
)

global current_state, last_state
current_state, last_state = States.Stop, States.Stop

rc = racecar_core.create_racecar()

line_follower = line_follow(rc, color_queue)

"""
This function is run once every time the start button is pressed
"""
def start():
    global current_state
    # Have the car begin at a stop
    rc.drive.stop()

    current_state = States.Line_Follow

    # Feature Initialization
    line_follower.start()

    # Print start message
    print(">> Final Challenge - Grand Prix")

"""
After start() is run, this function is run every frame until the back button
is pressed
"""
def update():
    global current_state
    if(current_state == States.Stop):
        rc.drive.stop()
    if(current_state == States.Line_Follow):
        current_state = line_follower.update()
    
"""
DO NOT MODIFY: Register start and update and begin execution
"""
if __name__ == "__main__":
    rc.set_start_update(start, update, None)
    rc.go()
