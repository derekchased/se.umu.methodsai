import math

import numpy as np

from OccupancyGrid import OccupancyGrid
from robot import Robot


class LaserSensorModel:
    
    BEAM_MAX_DISTANCE = 40

    # 'depth' of an obstacle.
    OBSTACLE_DEPTH_WCS = .8

    # half of the 'width' of the laser beam in radians.
    BEAM_WIDTH_RAD = (0.5 * np.pi) / 180

    # The maximum probability to assign to obstacles.
    # This prevents grid value from becoming 1 and never changing afterwards
    PROB_MAX = 0.98
    

    def __init__(self, robot: Robot, occupancy_grid: OccupancyGrid):
        self.__robot = robot
        self.__grid = occupancy_grid

        self.__beam_max_grid_distance = (self.BEAM_MAX_DISTANCE / occupancy_grid.cell_size)

    def update_grid(self):
        
        # Get robot heading angle.
        heading = self.__robot.getHeading()

        # Get robot XY position
        position_wcs = self.__robot.getPosition()

        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__grid.pos_to_grid(position_wcs['X'], position_wcs['Y'])
        
        # Get the distances of all laser beams in meters (?)
        beam_distances_wcs = np.array(self.__robot.getLaser()['Echoes'])

        # get the angle of each laser beam
        laser_angles = np.array(self.__robot.getLaserAngles())
        beam_angle_rads = laser_angles + heading
        
        # The x,y location an obstacle was detected at.
        obstacle_x_start_wcs = beam_distances_wcs * np.cos(beam_angle_rads)
        obstacle_y_start_wcs = beam_distances_wcs * np.sin(beam_angle_rads)
        
        # Corner 1 of the triangle to update
        obstacle_x_end_left_wcs = np.minimum((beam_distances_wcs + self.OBSTACLE_DEPTH_WCS), self.BEAM_MAX_DISTANCE) * np.cos(beam_angle_rads - self.BEAM_WIDTH_RAD)
        obstacle_y_end_left_wcs = np.minimum((beam_distances_wcs + self.OBSTACLE_DEPTH_WCS), self.BEAM_MAX_DISTANCE) * np.sin(beam_angle_rads - self.BEAM_WIDTH_RAD)
        
        # Corner 2 of the triangle to update
        obstacle_x_end_right_wcs = np.minimum((beam_distances_wcs + self.OBSTACLE_DEPTH_WCS), self.BEAM_MAX_DISTANCE) * np.cos(beam_angle_rads + self.BEAM_WIDTH_RAD)
        obstacle_y_end_right_wcs = np.minimum((beam_distances_wcs + self.OBSTACLE_DEPTH_WCS), self.BEAM_MAX_DISTANCE) * np.sin(beam_angle_rads + self.BEAM_WIDTH_RAD)

        # Convert coordinates to grid
        obstacle_x_start_grid, obstacle_y_start_grid = self.__grid.pos_to_grid_np(obstacle_x_start_wcs, obstacle_y_start_wcs)
        obstacle_x_end_left_grids, obstacle_y_end_left_grids = self.__grid.pos_to_grid_np(obstacle_x_end_left_wcs, obstacle_y_end_left_wcs)
        obstacle_x_end_right_grids, obstacle_y_end_right_grids = self.__grid.pos_to_grid_np(obstacle_x_end_right_wcs, obstacle_y_end_right_wcs)

        # Distance to obstacle
        obstacle_distance_grids = np.sqrt((obstacle_x_start_grid - robot_x_grid) ** 2 + (obstacle_y_start_grid - robot_y_grid) ** 2)
        
        # Decrease obstacle probability between the robot and the obstacle
        #for x, y in self.__triangle(


        """print("robot_x_grid",int(robot_x_grid))
                                print("robot_y_grid",int(robot_y_grid))
                                print("obstacle_x_end_left_grids",obstacle_x_end_left_grids.shape,obstacle_x_end_left_grids.astype(int))
                                print("obstacle_y_end_left_grids",obstacle_y_end_left_grids.shape, obstacle_y_end_left_grids.astype(int))
                                print("obstacle_x_end_right_grids",obstacle_x_end_right_grids.shape,obstacle_x_end_right_grids.astype(int))
                                print("obstacle_y_end_right_grids",obstacle_y_end_right_grids.shape,obstacle_y_end_right_grids.astype(int))"""

        #for x, y in vtri(int(robot_x_grid), int(robot_y_grid),obstacle_x_end_left_grids.astype(int), obstacle_y_end_left_grids.astype(int),obstacle_x_end_right_grids.astype(int), obstacle_y_end_right_grids.astype(int)):            # distance from robot to point on grid
        # Decrease obstacle probability between the robot and the obstacle
        
        robot_x_grid_int = int(robot_x_grid)
        robot_y_grid_int = int(robot_y_grid)

        for obstacle_x_end_left_grid, obstacle_y_end_left_grid, obstacle_x_end_right_grid, obstacle_y_end_right_grid, obstacle_distance_grid, beam_angle_rad in zip(obstacle_x_end_left_grids.astype(int), obstacle_y_end_left_grids.astype(int), obstacle_x_end_right_grids.astype(int), obstacle_y_end_right_grids.astype(int), obstacle_distance_grids, beam_angle_rads):
            for x, y in self.__triangle(
                    robot_x_grid_int, robot_y_grid_int,
                    obstacle_x_end_left_grid, obstacle_y_end_left_grid,
                    obstacle_x_end_right_grid, obstacle_y_end_right_grid
            ):
                # distance from robot to point on grid
                # r from lecture 7, slide 13
                distance = np.sqrt((x - robot_x_grid) ** 2 + (y - robot_y_grid) ** 2)

                # (R - r)/R from lecture 7, slide 13
                distance_term = (max(self.__beam_max_grid_distance - distance, 0) / self.__beam_max_grid_distance)

                # Angle between the laser beam an the current grid coordinate.
                # This does not seem to work.
                # alpha from lecture 7, slide 13
                angle = abs(np.arctan2(y - robot_y_grid, x - robot_x_grid))#-beam_angle_rad)

                # (beta - alpha)/beta from lecture 7, slide 13
                angle_term = ((self.BEAM_WIDTH_RAD - angle) / self.BEAM_WIDTH_RAD)
                #angle_term = 1

                if distance < obstacle_distance_grid:
                    # Region II: grid probably empty
                    prob_empty = (distance_term + angle_term) / 2
                    prob_occupied = 1 - prob_empty
                else:
                    # Region I: Grid probably occupied
                    prob_occupied = ((distance_term + angle_term) / 2) * self.PROB_MAX

                self.__grid.update_cell(x, y, prob_occupied)

    def __triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        """
        Returns all grid points in the triangle defined by the points (x1, y1), (x2, y2), (x3, y3)

        http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html
        http://www.sunshine2k.de/Files/TriangleRasterization.zip
        """
        # Sort points by ascending y. Assures that y1 <= y2 <= y3.
        points = [(x1, y1), (x2, y2), (x3, y3)]
        points.sort(key=lambda tup: tup[1])

        x1 = points[0][0]
        y1 = points[0][1]
        x2 = points[1][0]
        y2 = points[1][1]
        x3 = points[2][0]
        y3 = points[2][1]

        if y2 == y3:
            # flat bottom triangle
            yield from self.__triangle_flat(x1, y1, x2, y2, x3, y3)
        elif y1 == y2:
            # flat top triangle
            yield from self.__triangle_flat(x3, y3, x1, y1, x2, y2)
        else:
            # split triangle into flat-bottom and flat-top triangle.
            x_tmp = int(x1 + (float(y2 - y1) / float(y3 - y1)) * (x3 - x1))
            y_tmp = y2

            yield from self.__triangle_flat(x1, y1, x2, y2, x_tmp, y_tmp)
            yield from self.__triangle_flat(x3, y3, x2, y2, x_tmp, y_tmp)

    def __triangle_flat(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        changed1 = False
        changed2 = False

        dx1 = abs(x2 - x1)
        dy1 = abs(y2 - y1)
        dx2 = abs(x3 - x1)
        dy2 = abs(y3 - y1)

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

        for i in range(0, dx1 + 1):
            for x in range(min(curr_x1, curr_x2), max(curr_x1, curr_x2) + 1):
                yield x, curr_y2

            while e1 >= 0:
                if changed1:
                    curr_x1 += sign_x1
                else:
                    curr_y1 += sign_y1
                e1 -= (2 * dx1)

            if changed1:
                curr_y1 += sign_y1
            else:
                curr_x1 += sign_x1

            e1 += (2 * dy1)

            while curr_y2 != curr_y1:
                while e2 >= 0:
                    if changed2:
                        curr_x2 += sign_x2
                    else:
                        curr_y2 += sign_y2
                    e2 -= (2 * dx2)

                if changed2:
                    curr_y2 += sign_y2
                else:
                    curr_x2 += sign_x2

                e2 += (2 * dy2)