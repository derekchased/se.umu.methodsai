from collections import deque
from enum import Enum

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
    UNKNOWN_UPPER_BOUND = 0.55
    UNKNOWN_LOWER_BOUND = 0.45

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

        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__grid.pos_to_grid(position_wcs['X'], position_wcs['Y'])
        robot_coords = (int(robot_x_grid), int(robot_y_grid))

        grid = self.__grid.get_grid()
        mark_grid = np.full(grid.shape, Mark.NONE)

        frontiers = []

        queue_m = deque()

        queue_m.append(robot_coords)
        self.__set_mark(mark_grid, robot_coords, Mark.MAP_OPEN_LIST)

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

        for frontier in frontiers:
            frontier_medians.append(np.median(frontier, axis=0))

        frontier_medians = np.array(frontier_medians)

        # Sort based on distance to robot
        euclid_distances = np.apply_along_axis(self.__distance_sq, 1, frontier_medians, (robot_x_grid, robot_y_grid))
        order = np.argsort(euclid_distances)
        sorted_frontier_medians = frontier_medians[order]

        return sorted_frontier_medians


    def __distance_sq(self, point1, point2):
        dx = point1[0] - point2[0]
        dy = point1[0] - point2[0]

        return dx**2 + dy**2

    def __get_mark(self, mark_grid, position):
        return mark_grid[position[0]][position[1]]

    def __set_mark(self, mark_grid, position, mark):
        mark_grid[position[0]][position[1]] = mark

    def __is_frontier_point(self, position):
        """
        Returns whether a point is a frontier.
        A frontier point is an unknown point with at least one open-space neighbour
        """
        grid = self.__grid.get_grid()

        value = grid[position[0], position[1]]

        if self.UNKNOWN_LOWER_BOUND < value < self.UNKNOWN_UPPER_BOUND:
            neighbours = self.__get_neighbours(position)

            for point in neighbours:
                value = grid[point[0], point[1]]

                if value < self.UNKNOWN_LOWER_BOUND:
                    return True
        return False

    def __get_neighbours(self, position):
        """
        Return all neighbours of a position within grid bounds (4-connected)
        """
        x = position[0]
        y = position[1]
        max_x, max_y = self.__grid.get_size()

        neighbours = []

        if x > 0:
            neighbours.append((x - 1, y))
        if y > 0:
            neighbours.append((x, y - 1))
        if x + 1 < max_x:
            neighbours.append((x + 1, y))
        if y + 1 < max_y:
            neighbours.append((x, y + 1))

        return neighbours
