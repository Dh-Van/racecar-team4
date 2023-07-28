import sys
from typing import List, Tuple
from nptyping import NDArray

sys.path.insert(0, "../../../library")
import racecar_core, racecar_utils as rc_utils

"""
Returns the largest contour in the given image, that matches the given color range.
minimum area size is not required, will be set by default to 30
"""
def find_contour(
        color: List[tuple], image: NDArray, min_area = 30
    ) -> Tuple[NDArray, Tuple[int, int], float]:
    # When the image is not found: None, None is returned
    if image is None:
        return None, None, None
        
    # Find all contours of given color
    list_contours = rc_utils.find_contours(image, color[0], color[1])

    # Gets the largest contour
    contour = rc_utils.get_largest_contour(list_contours, min_area)

    # If no contour was found: None, None is returned
    if(contour is None):
        # print("No contour found")
        return None, None, -1

    # Gets information about the center and area
    contour_center = rc_utils.get_contour_center(contour)
    contour_area = rc_utils.get_contour_area(contour)

    # Returns the largest contour center and area
    return contour, contour_center, contour_area

"""
Returns the output in the order of the input of windows
"""
def get_lidar_distances(scan, windows):
    output = []
    for window in windows:
        __, dist = rc_utils.get_lidar_closest_point(scan, window)
        output.append(dist)

    return output