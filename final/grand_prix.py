"""
Copyright MIT and Harvey Mudd College
MIT License
Fall 2020

Final Challenge - Grand Prix
"""
# Imports
import sys
sys.path.insert(0, "../../library")
sys.path.insert(1, "features")
sys.path.insert(2, "utils")


from line_following import line_follow
from wall_follwing import wall_follow
from states import States
from ar_markers import ar_scan
from lane_follow import lane_follow
import constants
import racecar_core
import racecar_utils as rc_utils

# Global variables
color_queue = (
    (constants.RED_LINE, constants.YELLOW_LINE), 
    (constants.YELLOW_LINE, constants.GREEN_LINE), 
    (constants.GREEN_LINE, constants.RED_LINE),
    (constants.RED_LINE, constants.GREEN_LINE),
    (constants.GREEN_LINE, constants.HSV_EVERYTHING)
)

global current_state, last_state
current_state, last_state = States.Stop, States.Stop

rc = racecar_core.create_racecar()
global ar_id
line_follower = line_follow(rc, color_queue)
lane_follower = lane_follow(rc)
wall_follower = wall_follow(rc)
ar_scanner = ar_scan(rc)
ar_id = 0

"""
This function is run once every time the start button is pressed
"""
def start():
    global current_state
    rc.set_update_slow_time(0.25)
    # Have the car begin at a stop
    rc.drive.stop()

    current_state = States.Lane_Follow

    # Feature Initialization
    line_follower.start()
    wall_follower.start()

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
    if(current_state == States.Wall_Follow):
        current_state = wall_follower.update()
    if(current_state == States.Lane_Follow):
        current_state = lane_follower.update()
    
def update_slow():
#     global current_state
#     marker_list = ar_scanner.scan()
#     red_marker = ar_scanner.get_color(ar_scanner.get_marker_list, constants.RED_BORDER, "Red")
#     if(red_marker is not None and red_marker.get_id() == 2):
#         current_state = States.Wall_Follow
    pass

"""
DO NOT MODIFY: Register start and update and begin execution
"""
if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
