from robot import Robot
import numpy as np
from OccupancyGrid import OccupancyGrid

class ObstacleAvoider:

    def __init__(self, robot: Robot, occupancy_grid: OccupancyGrid):
        self.__robot = robot
        self.__grid = occupancy_grid
        self.__danger_threshold = .5
        self.__warning_threshold = .9

    def in_danger(self):
        """
        Returns true if the robot is in danger of colliding with an obstacle.
        If this has been set to true, path planning and frontier detection should reoccur.
        """
        
        # Calculate the robot's position on the grid.
        # heading = self.__robot.getHeading()
        position_wcs = self.__robot.getPosition()
        robot_col, robot_row = self.__grid.wcs_to_grid(position_wcs['X'], position_wcs['Y'])

        # Get the distances of all laser beams in meters
        beam_distances_wcs = np.array(self.__robot.getLaser()['Echoes'])
        
        in_warning_range = np.any(beam_distances_wcs <= self.__warning_threshold)

        in_danger_range = np.any(beam_distances_wcs <= self.__danger_threshold)

        if in_danger_range or in_warning_range:
            print("in_warning_range:",in_warning_range,"in_danger_range:",in_danger_range, "distance to obstacles:", beam_distances_wcs[beam_distances_wcs<=self.__warning_threshold])

        #print("\nin_danger_range",in_danger_range, beam_distances_wcs[np.where(beam_distances_wcs <= self.__threshold)])
        #print(np.sort(beam_distances_wcs[beam_distances_wcs < 2]))

        return in_danger_range, in_warning_range

    def loop(self):
        """
        If `in_danger` returns True, this function gets complete control of the robot until the robot is not in danger
        anymore.
        """

        # Move in such a way that the in_danger is not firing anymore.

        


    def distance_2d(self, x_point, y_point, x, y):
        """
        Returns the distance between two points defined by (x_point, y_point) and (x, y).
        """
        return np.hypot(x - x_point, y - y_point)

    def norm_angle(self, angle):
        """
        Wraps an angle in radians to a value between -pi and pi.
        """
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def angle_2d(self, x_point, y_point, x, y):
        """
        Returns the angle of the vector from (x_point, y_point) to (x, y)
        """
        return np.arctan2(y - y_point, x - x_point)