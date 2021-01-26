import math

import numpy as np

from OccupancyGrid import OccupancyGrid
from robot import Robot


class LaserSensorModel:
    
    BEAM_MAX_DISTANCE = 40

    # 'depth' of an obstacle.
    OBSTACLE_DEPTH_WCS = .5

    # the 'width' of the laser beam in radians.
    BEAM_WIDTH_RAD = np.pi / 180

    # The maximum probability to assign to obstacles.
    # This prevents grid value from becoming 1 and never changing afterwards
    PROB_MAX = 0.98
    

    def __init__(self, robot: Robot, occupancy_grid: OccupancyGrid):
        self.__robot = robot
        self.__grid = occupancy_grid

        self.__beam_max_grid_distance = (self.BEAM_MAX_DISTANCE / occupancy_grid.cell_size)
        self.__obstacle_depth_grid = self.OBSTACLE_DEPTH_WCS / occupancy_grid.cell_size

    def update_grid(self):
        
        # Get robot heading angle.
        heading = self.__robot.getHeading()

        # Get robot XY position
        position_wcs = self.__robot.getPosition()

        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__grid.pos_to_grid(position_wcs['X'], position_wcs['Y'])
        
        # Get the distances of all laser beams in meters
        beam_distances_wcs = np.array(self.__robot.getLaser()['Echoes'])

        rows, cols = self.__grid.get_size()

        result = np.ones(shape=(rows, cols)) * 0.5

        ys, xs = np.ogrid[0:rows, 0:cols]

        distances = self.distance_2d(robot_x_grid, robot_y_grid, xs, ys)
        angles = self.norm_angle(self.angle_2d(robot_x_grid, robot_y_grid, xs, ys) - heading)
        beams = np.round(angles / self.BEAM_WIDTH_RAD)

        beam_angles = self.norm_angle(angles - (beams * self.BEAM_WIDTH_RAD))

        beam_indices = beams.astype(np.int)
        beam_indices[abs(beam_indices) > 135] = -135
        beam_indices += 135

        laser_distances = beam_distances_wcs[beam_indices] / self.__grid.cell_size

        angle_mask = np.less(np.abs(beams), 135)
        region_I_mask = angle_mask & np.less(laser_distances, self.__beam_max_grid_distance) & np.less(np.abs(laser_distances - distances), self.__obstacle_depth_grid)
        region_II_mask = angle_mask & np.less(distances, laser_distances)
        region_III_mask = ~(region_II_mask | region_I_mask)

        distance_term = self.distance_term(distances, np.amax(distances))
        angle_term = self.angle_term(beam_angles, np.amax(beam_angles) * 2)

        np.putmask(result, region_I_mask, (distance_term + angle_term) / 2 * self.PROB_MAX)
        np.putmask(result, region_II_mask, 1 - (distance_term + angle_term) / 2)

        #self.__grid.set_grid(region_III_mask)
        self.__grid.update_grid(result, region_III_mask)


    def norm_angle(self, angle):
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def distance_term(self, distance_grid, max_value):
        return (max_value - distance_grid) / max_value

    def angle_term(self, angle_grid, max_value):
        return (max_value - np.abs(angle_grid)) / max_value

    def distance_2d(self, x_point, y_point, x, y):
        return np.hypot(x - x_point, y - y_point)

    def angle_2d(self, x_point, y_point, x, y):
        return np.arctan2(y - y_point, x - x_point)

    def pol2cart(self, rs, thetas):
        return rs * np.cos(thetas), rs * np.sin(thetas)