import numpy as np

from OccupancyGrid import OccupancyGrid
from robot import Robot


class LaserSensorModel:
    BEAM_MAX_DISTANCE = 40

    def __init__(self, robot: Robot, occupancy_grid: OccupancyGrid):
        self.__robot = robot
        self.__grid = occupancy_grid

        self.__beam_max_grid_distance = self.BEAM_MAX_DISTANCE / occupancy_grid.cell_size

    def update_grid(self):
        # get the angle of each laser beam
        laser_angles = self.__robot.getLaserAngles()
        # Get the distances of all laser beams in meters (?)
        laser_scan = self.__robot.getLaser()['Echoes']

        # Get robot XY position
        position_wcs = self.__robot.getPosition()
        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__grid.pos_to_grid(position_wcs['X'], position_wcs['Y'])

        for angle, distance in zip(laser_angles, laser_scan):
            self.__process_beam(robot_x_grid, robot_y_grid, angle, distance)

    def __process_beam(self, robot_x_grid, robot_y_grid, beam_angle, beam_distance):
        # Assumed distance error in laser measurement. Obstacle size on grid is taken as 2*distance_error.
        distance_error = 0.5

        # The maximum probability to assign to obstacles.
        # This prevents grid value from becoming 1 and never changing afterwards
        prob_max = 0.98

        obstacle_x_start_wcs = (beam_distance - distance_error) * np.cos(beam_angle)
        obstacle_y_start_wcs = (beam_distance - distance_error) * np.sin(beam_angle)
        obstacle_x_end_wcs = (beam_distance + distance_error) * np.cos(beam_angle)
        obstacle_y_end_wcs = (beam_distance + distance_error) * np.sin(beam_angle)

        obstacle_x_start_grid, obstacle_y_start_grid = self.__grid.pos_to_grid(obstacle_x_start_wcs, obstacle_y_start_wcs)
        obstacle_x_end_grid, obstacle_y_end_grid = self.__grid.pos_to_grid(obstacle_x_end_wcs, obstacle_y_end_wcs)

        # Decrease obstacle probability between the robot and the obstacle
        for x, y in self.__line(robot_x_grid, robot_y_grid, obstacle_x_start_grid, obstacle_y_start_grid):
            distance = np.sqrt((x - robot_x_grid) ** 2 + (y - robot_y_grid) ** 2)

            prob_empty = (((self.__beam_max_grid_distance - distance) / self.__beam_max_grid_distance) + 1) / 2
            prob_occupied = 1 - prob_empty

            self.__grid.update_cell(x, y, prob_occupied)

        if beam_distance >= self.__beam_max_grid_distance:
            return

        # Increase obstacle probability at the point of the obstacle
        for x, y in self.__line(obstacle_x_start_grid, obstacle_y_start_grid, obstacle_x_end_grid, obstacle_y_end_grid):
            distance = np.sqrt((x - robot_x_grid) ** 2 + (y - robot_y_grid) ** 2)

            prob_occupied = ((((self.__beam_max_grid_distance - distance) / self.__beam_max_grid_distance) + 1) / 2) * prob_max

            self.__grid.update_cell(x, y, prob_occupied)

    def __line(self, x0: int, y0: int, x1: int, y1: int):
        """
        Bresenham's line algorithm.
        """
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                return self.__line_low(x1, y1, x0, y0)
            else:
                return self.__line_low(x0, y0, x1, y1)
        else:
            if y0 > y1:
                return self.__line_high(x1, y1, x0, y0)
            else:
                return self.__line_high(x0, y0, x1, y1)

    def __line_low(self, x0: int, y0: int, x1: int, y1: int):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1

        if dy < 0:
            yi = -1
            dy = -dy

        D = (2 * dy) - dx
        y = y0

        for x in range(x0, x1):
            yield x, y
            if D > 0:
                y = y + yi
                D = D + (2 * (dy - dx))
            else:
                D = D + 2 * dy

    def __line_high(self, x0: int, y0: int, x1: int, y1: int):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1

        if dx < 0:
            xi = -1
            dx = -dx

        D = (2 * dx) - dy
        x = x0

        for y in range(y0, y1):
            yield x, y
            if D > 0:
                x = x + xi
                D = D + (2 * (dx - dy))
            else:
                D = D + 2 * dx
