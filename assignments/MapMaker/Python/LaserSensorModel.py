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
        x_rcs, y_rcs = self.__grid.wcs_to_grid(position_wcs['X'], position_wcs['Y'])
        
        # Get the distances of all laser beams in meters
        beam_distances_wcs = np.array(self.__robot.getLaser()['Echoes'])

        rows, cols = self.__grid.get_size() # height, width

        # Check this regarding ogrid, 
        # https://towardsdatascience.com/the-little-known-ogrid-function-in-numpy-19ead3bdae40
        # "One important note is the direction of the axes in Numpy. Contrary to how we
        # are used to seeing x and y axes, the axes in a Numpy image are as below:" 
        # -> https://miro.medium.com/max/303/1*GMUpEYbk6PX01RF7Fs2wNQ.png
        ys, xs = np.ogrid[0:rows, 0:cols]

        # A grid where the value of each pixel is the distance between it and the robot
        distances = self.distance_2d(x_rcs, y_rcs, xs, ys)

        # A grid where the value of each pixel is the angle between it and the robot's heading.
        angles = self.norm_angle(self.angle_2d(x_rcs, y_rcs, xs, ys) - heading)

        # A grid where the value of each pixel is the angle in integer degrees
        # between it and the heading of the robot from (-180 to 180)
        beams = np.round(angles / self.BEAM_WIDTH_RAD)

        # A grid where the value of each pixel is the angle between the angle from the robot to the pixel
        # and the angle from the robot to the laser beam closest to the pixel
        beam_angles = self.norm_angle(angles - (beams * self.BEAM_WIDTH_RAD))

        # A grid where the value of each pixel is the index of the laser beam that reaches that pixel
        beam_indices = beams.astype(np.int)
        beam_indices[abs(beam_indices) > 135] = -135
        beam_indices += 135

        # A grid containing the distance that each laser reaches in that direction.
        laser_distances = beam_distances_wcs[beam_indices] / self.__grid.cell_size

        # A boolean mask for the pacman-shaped slice around the robot that the laser beams reach.
        angle_mask = np.less(np.abs(beams), 135)

        # A boolean mask for regions I, II and III of the entire grid.
        # Region I (lecture 7, slide 13) is the region where obstacles were detected.
        region_I_mask = angle_mask & np.less(laser_distances, self.__beam_max_grid_distance) & np.less(np.abs(laser_distances - distances), self.__obstacle_depth_grid)

        # Region II (lecture 7, slide 14) is the region between the robot and the obstacles.
        region_II_mask = angle_mask & np.less(distances, laser_distances)

        # Region III is the region where this measurement does not provide any information
        # (behind the robot and behind the obstacles)
        region_III_mask = ~(region_II_mask | region_I_mask)

        # The distance term (R - r)/R for the probability calculation as specified in lecture 7 slide 13 and 14
        distance_term = self.distance_term(distances, np.amax(distances))
        # The angle term (Beta - alpha)/Beta for the probability calculation as specified in lecture 7 slide 13 and 14
        angle_term = self.angle_term(beam_angles, np.amax(beam_angles) * 2)

        # The grid that we want to return
        result = np.ones(shape=(rows, cols)) * 0.5

        # Updating each pixel in region I and region II as specified in the slides of lecture 7
        np.putmask(result, region_I_mask, (distance_term + angle_term) / 2 * self.PROB_MAX)
        np.putmask(result, region_II_mask, 1 - (distance_term + angle_term) / 2)

        #self.__grid.set_grid(region_III_mask)
        self.__grid.update_grid(result, ~region_III_mask)

    def norm_angle(self, angle):
        """
        Wraps an angle in radians to a value between -pi and pi.
        """
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def distance_term(self, distance_grid, max_value):
        """
        Distance term as provided in equation in lecture 7, slide 13 and 14.
        """
        return (max_value - distance_grid) / max_value

    def angle_term(self, angle_grid, max_value):
        """
        Angle term as provided in equation in lecture 7, slide 13 and 14.
        """
        return (max_value - np.abs(angle_grid)) / max_value

    def distance_2d(self, x_point, y_point, x, y):
        """
        Returns the distance between two points defined by (x_point, y_point) and (x, y).
        """
        return np.hypot(x - x_point, y - y_point)

    def angle_2d(self, x_point, y_point, x, y):
        """
        Returns the angle of the vector from (x_point, y_point) to (x, y)
        """
        return np.arctan2(y - y_point, x - x_point)

    def pol2cart(self, r, theta):
        """
        Converts polar coordinates (r, theta) to cartesian (x, y).
        """
        return r * np.cos(theta), r * np.sin(theta)
