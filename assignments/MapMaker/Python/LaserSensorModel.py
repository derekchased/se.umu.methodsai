import math

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

        # Get robot heading angle.
        heading = self.__robot.getHeading()

        # Get robot XY position
        position_wcs = self.__robot.getPosition()
        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__grid.pos_to_grid(position_wcs['X'], position_wcs['Y'])

        for angle, distance in zip(laser_angles, laser_scan):
            self.__process_beam(robot_x_grid, robot_y_grid, angle + heading, distance)



    def __process_beam(self, robot_x_grid, robot_y_grid, beam_angle, beam_distance):
        # Assumed distance error in laser measurement. Obstacle size on grid is taken as 2*distance_error.
        distance_error = 0.5
        # half of the 'width' of the laser beam in radians.
        beam_width = (0.5 * np.pi) / 180

        # The maximum probability to assign to obstacles.
        # This prevents grid value from becoming 1 and never changing afterwards
        prob_max = 0.98

        obstacle_x_start_wcs = max((beam_distance - distance_error), 0) * np.cos(beam_angle)
        obstacle_y_start_wcs = max((beam_distance - distance_error), 0) * np.sin(beam_angle)
        obstacle_x_end_wcs = min((beam_distance + distance_error), self.BEAM_MAX_DISTANCE - distance_error) * np.cos(beam_angle)
        obstacle_y_end_wcs = min((beam_distance + distance_error), self.BEAM_MAX_DISTANCE - distance_error) * np.sin(beam_angle)
        # obstacle_x_start_left_wcs = max((beam_distance - distance_error), 0) * np.cos(beam_angle - beam_width)
        # obstacle_y_start_left_wcs = max((beam_distance - distance_error), 0) * np.sin(beam_angle - beam_width)
        # obstacle_x_start_right_wcs = max((beam_distance - distance_error), 0) * np.cos(beam_angle + beam_width)
        # obstacle_y_start_right_wcs = max((beam_distance - distance_error), 0) * np.sin(beam_angle + beam_width)
        # obstacle_x_end_left_wcs = (beam_distance + distance_error) * np.cos(beam_angle - beam_width)
        # obstacle_y_end_left_wcs = (beam_distance + distance_error) * np.sin(beam_angle - beam_width)
        # obstacle_x_end_right_wcs = (beam_distance + distance_error) * np.cos(beam_angle + beam_width)
        # obstacle_y_end_right_wcs = (beam_distance + distance_error) * np.sin(beam_angle + beam_width)

        obstacle_x_start_grid, obstacle_y_start_grid = self.__grid.pos_to_grid(obstacle_x_start_wcs, obstacle_y_start_wcs)
        obstacle_x_end_grid, obstacle_y_end_grid = self.__grid.pos_to_grid(obstacle_x_end_wcs, obstacle_y_end_wcs)
        # obstacle_x_start_left_grid, obstacle_y_start_left_grid = self.__grid.pos_to_grid(obstacle_x_start_left_wcs, obstacle_y_start_left_wcs)
        # obstacle_x_start_right_grid, obstacle_y_start_right_grid = self.__grid.pos_to_grid(obstacle_x_start_right_wcs, obstacle_y_start_right_wcs)
        # obstacle_x_end_left_grid, obstacle_y_end_left_grid = self.__grid.pos_to_grid(obstacle_x_end_left_wcs, obstacle_y_end_left_wcs)
        # obstacle_x_end_right_grid, obstacle_y_end_right_grid = self.__grid.pos_to_grid(obstacle_x_end_right_wcs, obstacle_y_end_right_wcs)

        obstacle_start_distance = np.sqrt((obstacle_x_start_grid - robot_x_grid) ** 2 + (obstacle_y_start_grid - robot_y_grid) ** 2)

        # Decrease obstacle probability between the robot and the obstacle
        for x, y in self.__line(robot_x_grid, robot_y_grid, obstacle_x_end_grid, obstacle_y_end_grid):
            distance = np.sqrt((x - robot_x_grid) ** 2 + (y - robot_y_grid) ** 2)

            if distance < obstacle_start_distance:
                prob_empty = (((self.__beam_max_grid_distance - distance) / self.__beam_max_grid_distance) + 1) / 2
                prob_occupied = 1 - prob_empty
            else:
                prob_occupied = ((((self.__beam_max_grid_distance - distance) / self.__beam_max_grid_distance) + 1) / 2) * prob_max

            self.__grid.update_cell(x, y, prob_occupied)

    def __triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        points = [(x1, y1), (x2, y2), (x3, y3)]
        points.sort(key=lambda tup: tup[1])

        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[1][0]
        y2 = points[1][1]
        x3 = points[2][0]
        y3 = points[2][1]

        if y2 == y3:
            yield from self.__triangle_flat(x1, y1, x2, y2, x3, y3)
        elif y1 == y2:
            yield from self.__triangle_flat(x3, y3, x1, y1, x2, y2)
        else:
            x_tmp = int(x1 + (float(y2 - y1) / float(y3 - y1)) * (x3 - x1))
            y_tmp = y2

            yield from self.__triangle_flat(x1, y1, x2, y2, x_tmp, y_tmp)
            yield from self.__triangle_flat(x3, y3, x2, y2, x_tmp, y_tmp)

    def __triangle_flat(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        changed1 = False
        changed2 = False

        if (y2 != y3):
            print("what the fuck", y2, y3)
            raise Exception

        dx1 = abs(x2 - x1)
        dy1 = abs(y2 - x1)
        dx2 = abs(x3 - x1)
        dy2 = abs(y3 - x1)

        sign_x1 = np.sign(x2 - x1)
        sign_x2 = np.sign(x3 - x1)
        sign_y1 = np.sign(y2 - y1)
        sign_y2 = np.sign(y3 - y1)

        if dy1 > dx1:
            tmp = dx1
            dx1 = dy1
            dy1 = tmp
            changed1 = True

        if dy2 > dx2:
            tmp = dx2
            dx2 = dy2
            dy2 = tmp
            changed2 = True

        e1 = (2 * dy1) - dx1
        e2 = (2 * dy2) - dx2

        curr_x1 = x1
        curr_y1 = y1
        curr_x2 = x1
        curr_y2 = y1

        for i in range(0, dx1):
            # yield points in line
            for x in range(min(curr_x1, curr_x2), max(curr_x1, curr_x2) + 1):
                yield x, curr_y1

            while e1 >= 0:
                if changed1:
                    curr_x1 += sign_x1
                else:
                    curr_y1 += sign_y1
                e1 = e1 - (2 * dx1)

            if changed1:
                curr_y1 += sign_y1
            else:
                curr_x1 += sign_x1

            e1 = e1 + (2 * dy1)

            while curr_y2 != curr_y1:
                while e2 >= 0:
                    if changed2:
                        curr_x2 += sign_x2
                    else:
                        curr_y2 += sign_y2
                    e2 = e2 - (2 * dx2)

                if changed2:
                    curr_y2 += sign_y2
                else:
                    curr_x2 += sign_x2

                e2 = e2 + (2 * dy2)

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
