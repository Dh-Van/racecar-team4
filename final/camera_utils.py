import sys
sys.path.insert(0, "../../library")
import racecar_core
import racecar_utils as rc_utils
import constants

def find_contours(color, image, min_contour):    
    # When the image is not found: None, None is returned
    if image is None:
        return None, None
        
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])

    # Gets the largest contour
    contour = rc_utils.get_largest_contour(list_contours, 0)

    # If no contour was found: None, None is returned
    if(contour is None):
        print("No contour found")
        return None, -1

    # Gets information about the center and area
    contour_center = rc_utils.get_contour_center(contour)
    contour_area = rc_utils.get_contour_area(contour)

    # Returns the largest contour center and area
    return contour, contour_center, contour_area