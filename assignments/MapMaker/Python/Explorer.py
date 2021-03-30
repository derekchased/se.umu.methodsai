from collections import deque
from enum import Enum

import NPFunctions
from OccupancyGrid import OccupancyGrid
from robot import Robot
import numpy as np


class Mark(Enum):
    NONE = 0
    MAP_OPEN_LIST = 1
    MAP_CLOSE_LIST = 2
    FRONTIER_OPEN_LIST = 3
    FRONTIER_CLOSE_LIST = 4


class Explorer:

    # Upper and lower bound on cell value for determining
    # whether a cell on the map is 'unknown' for determining frontiers
    # See also: __is_frontier_point()
    UNKNOWN_UPPER_BOUND = 0.65
    UNKNOWN_LOWER_BOUND = 0.35

    def __init__(self, robot: Robot, grid: OccupancyGrid):
        self.__robot = robot
        self.__grid = grid

    def get_frontiers(self):
        """
        Returns a list of all frontiers on the current map, ordered by euclidian distance to the median of the frontier,
        in ascending order.

        Algorithm based on: https://arxiv.org/ftp/arxiv/papers/1806/1806.03581.pdf
        """

        print("Determining frontiers..")

        # Get robot XY position
        position_wcs = self.__robot.getPosition()
        heading = self.__robot.getHeading()

        # Calculate the robot's position on the grid.
        robot_col, robot_row = self.__grid.wcs_to_grid(position_wcs['X'], position_wcs['Y'])

        grid = self.__grid.get_grid()
        mark_grid = np.full(grid.shape, Mark.NONE)

        frontiers = []

        initial_coords = self.__determine_start_coords((robot_col, robot_row), grid.shape, heading)

        queue_m = deque()
        queue_m.append(initial_coords)
        self.__set_mark(mark_grid, initial_coords, Mark.MAP_OPEN_LIST)

        while len(queue_m) > 0:
            p = queue_m.popleft()

            if self.__get_mark(mark_grid, p) == Mark.MAP_CLOSE_LIST:
                continue

            if self.__is_frontier_point(p):
                queue_f = deque()
                new_frontier = []

                queue_f.append(p)
                self.__set_mark(mark_grid, p, Mark.FRONTIER_OPEN_LIST)

                while len(queue_f) > 0:
                    q = queue_f.popleft()

                    q_mark = self.__get_mark(mark_grid, q)

                    if q_mark == Mark.MAP_CLOSE_LIST or q_mark == Mark.FRONTIER_CLOSE_LIST:
                        continue

                    if self.__is_frontier_point(q):
                        new_frontier.append(q)
                        q_neighbours = self.__get_neighbours(q)

                        for w in q_neighbours:
                            w_mark = self.__get_mark(mark_grid, w)

                            if w_mark != Mark.FRONTIER_OPEN_LIST and w_mark != Mark.FRONTIER_CLOSE_LIST and w_mark != Mark.MAP_CLOSE_LIST:
                                queue_f.append(w)
                                self.__set_mark(mark_grid, w, Mark.FRONTIER_OPEN_LIST)
                    self.__set_mark(mark_grid, q, Mark.FRONTIER_CLOSE_LIST)

                # Mark all points of new_frontier as MAP_CLOSE_LIST
                for frontier_point in new_frontier:
                    self.__set_mark(mark_grid, frontier_point, Mark.MAP_CLOSE_LIST)

                frontiers.append(new_frontier)

            p_neighbours = self.__get_neighbours(p)

            for v in p_neighbours:
                v_mark = self.__get_mark(mark_grid, v)

                if v_mark != Mark.MAP_OPEN_LIST and v_mark != Mark.MAP_CLOSE_LIST:
                    v_neighbours = self.__get_neighbours(v)

                    # If v has at least one MAP_OPEN_SPACE neighbour, then append v to queue_m
                    for x in v_neighbours:
                        if self.__get_mark(mark_grid, x) == Mark.MAP_OPEN_LIST:
                            queue_m.append(v)
                            self.__set_mark(mark_grid, v, Mark.MAP_OPEN_LIST)
                            break

            self.__set_mark(mark_grid, p, Mark.MAP_CLOSE_LIST)

        if len(frontiers) == 0:
            return []

        frontier_medians = []

        # Only select frontier medians that are in open space. This is because the wavefront planner cannot deal
        # with unknown areas.
        for frontier in frontiers:
            # Skip very small frontiers
            if len(frontier) < 6:
                continue

            median = np.median(frontier, axis=0).astype(int)

            # Only add frontiers that are in open areas
            if grid[median[0], median[1]] <= Explorer.UNKNOWN_LOWER_BOUND:
                frontier_medians.append(median)

        if len(frontier_medians) == 0:
            return [initial_coords]

        frontier_medians = np.array(frontier_medians)

        # Sort based on distance to robot
        euclid_distances = np.apply_along_axis(NPFunctions.distance_sq, 1, frontier_medians, initial_coords)
        order = np.argsort(euclid_distances)
        sorted_frontier_medians = frontier_medians[order]

        return sorted_frontier_medians

    def __determine_start_coords(self, robot_coords, grid_shape, heading):
        """
        Returns the coordinates closest to the robot that are still on the map.
        This only returns something different when the robot is off the map.
        """
        col = robot_coords[0]
        row = robot_coords[1]

        # Move the starting point to be 3 grid cells in front of the robot. Grid cell directly under the robot
        # could be unknown.
        col = col + (3 * np.sin(heading))
        row = row + (3 * np.cos(heading))

        if col < 0:
            col = 0
        if col > grid_shape[0] - 1:
            col = grid_shape[0] - 1
        if row < 0:
            row = 0
        if row > grid_shape[1] - 1:
            row = grid_shape[1] - 1

        return int(col), int(row)

    def __get_mark(self, mark_grid, position):
        return mark_grid[position[0]][position[1]]

    def __set_mark(self, mark_grid, position, mark):
        mark_grid[position[0]][position[1]] = mark

    def __is_frontier_point(self, position):
        """
        Returns whether a point is a frontier.
        A frontier point is an open-space point with at least one unknown neighbour
        """
        grid = self.__grid.get_grid()

        value = grid[position[0], position[1]]

        if value < self.UNKNOWN_LOWER_BOUND:
            neighbours = self.__get_neighbours(position)

            for point in neighbours:
                value = grid[point[0], point[1]]

                if self.UNKNOWN_LOWER_BOUND < value < self.UNKNOWN_UPPER_BOUND:
                    return True
        return False

    def __get_neighbours(self, position):
        """
        Return all neighbours of a position within grid bounds (8-connected)
        """
        x = position[0]
        y = position[1]
        max_x, max_y = self.__grid.get_size()

        return NPFunctions.get_neighbours(x, y, max_x, max_y)
