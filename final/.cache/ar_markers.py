# Imports

#region
import sys, scipy, cv2, numpy as np
from typing import List, Tuple
sys.path.insert(0, "../../../library")
sys.path.insert(0, "..utils")
import constants, math_utils, sensor_utils
from states import States
import racecar_core
import racecar_utils as rc_utils
#endregion

class ar_scan:

    rc: racecar_core.Racecar = None
    marker_list: List[rc_utils.ARMarker] = []

    def __init__(self, racecar: racecar_core.Racecar) -> None:
        self.rc = racecar
    
    """
    Main method for getting the id of an ar marker. This method takes a color range and name
    as an input. It scans for all ar markers matching the color passed in and returns the 
    biggest marker of that color
    """
    def scan(self, color_range, color_name: str) -> int:
        image = self.rc.camera.get_color_image()

        aruco_data = cv2.aruco.detectMarkers(
            image,
            cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250),
            parameters=cv2.aruco.DetectorParameters_create()
        )
        
        self.marker_list = self.__get_marker_list(aruco_data)
        color_markers = []
        for marker in self.marker_list:
            color_tuple = [(color_range[0], color_range[1], color_name)]
            marker.detect_colors(image, color_tuple)
            if(marker.get_color == color_name): color_markers.append(marker)

        return self.__get_biggest_marker(color_markers)

    def __get_biggest_marker(self, marker_list: List[rc_utils.ARMarker]) -> int:
        biggest = 0, None
        for marker in marker_list:
            size = self.get_size(marker)
            if(size > biggest[0]):
                biggest = size, marker
        return biggest[1]

    def get_size(self, marker: rc_utils.ARMarker) -> int:
        corners = marker.get_corners()
        side_len = abs(corners[0][0] - corners[1][0])
        return side_len

    def __get_marker_list(self, aruco_data) -> List[rc_utils.ARMarker]:
        corners, ids = aruco_data[0], aruco_data[1]
        markers = []    

        for i in range(len(corners)):
            corner = corners[i][0].astype(np.int32)
            for j in range(len(corner)):
                corner[j] = [corner[j][1], corner[j][0]]
            id = ids[i]
            markers.append(rc_utils.ARMarker(id, corner))

        return markers