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

        return in_danger_range, in_warning_range
