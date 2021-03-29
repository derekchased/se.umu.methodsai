import NPFunctions
from robot import Robot
from OccupancyGrid import OccupancyGrid
from Explorer import Explorer
import numpy as np

class WavefrontPlanner:

    OPEN_CERTAINTY = Explorer.UNKNOWN_UPPER_BOUND

    def __init__(self, robot: Robot, occupancy_grid: OccupancyGrid):
        self.__robot = robot
        self.__occupancy_grid = occupancy_grid
        self.__wave_grid = np.zeros(occupancy_grid.get_size())


    def get_grid_path(self, frontier_x_grid: int, frontier_y_grid: int):
        # Get robot XY position
        position_wcs = self.__robot.getPosition()

        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__occupancy_grid.wcs_to_grid(position_wcs['X'], position_wcs['Y'])
        robot_x_grid = int(robot_x_grid)
        robot_y_grid = int(robot_y_grid)

        # Init "wave" grid to zeros
        self.__wave_grid = np.zeros(self.__occupancy_grid.get_grid().shape)

        # Set the robot's position on the grid to 1
        current_distance = 1
        self.__wave_grid[robot_x_grid, robot_y_grid] = current_distance
        goal_point_value = 0
        expand_wave = True
        
        while expand_wave:
            # get all x, y coordinates of elements with value == current_distance
            current_wave_coordinates = np.transpose((self.__wave_grid == current_distance).nonzero())

            # increment distance
            current_distance += 1
            updated_neighbors = []
            for neighbor_coordinates in current_wave_coordinates:
                x = neighbor_coordinates[0]
                y = neighbor_coordinates[1]

                # Update neighbors with new distance
                updated_neighbors += self.__update_neighbors(x, y, current_distance)

            # If no neighbors were updated then??
            if len(updated_neighbors) == 0:
                print("len(updated_neighbors) == 0")
                expand_wave = False
               #assert error
            else:
                goal_point_value = self.__wave_grid[frontier_x_grid, frontier_y_grid]

                if goal_point_value != 0:
                    expand_wave = False

        if goal_point_value < 0:
            print("goal_point_value < 0 (marked as obstacle)", current_distance)
            # TODO- goal point marked as an obstacle
            # select closest? choose different frontier node?
            assert error
        elif goal_point_value == 0:
            # TODO- goal point was not reached (perhaps surrounded by obstacles)
            # select closest? choose different frontier node?
            print("goal_point_value == 0 (not checked yet)", current_distance)
            assert error
        else:
            return self.__backtrack_path(frontier_x_grid, frontier_y_grid)

    def __update_neighbors(self, x, y, distance):
        open_neighbours = []
        neighbours = self.__get_neighbours(x, y)

        for neighbour in neighbours:
            if self.__wave_grid[neighbour[0], neighbour[1]] != 0:
                # Skip coordinates that already are assigned
                continue

            neighbour_value = self.__occupancy_grid.get_grid()[neighbour[0], neighbour[1]]
            neighbour_distance = -1

            if neighbour_value < self.OPEN_CERTAINTY:
                neighbour_distance = distance
                open_neighbours.append(neighbour)

            self.__wave_grid[neighbour[0], neighbour[1]] = neighbour_distance

        return open_neighbours

    def __get_neighbours(self, x, y):
        """
        Return all neighbours of a position within grid bounds (4-connected)
        """
        max_x, max_y = self.__occupancy_grid.get_size()

        neighbours = []

        left = x > 0
        right = x + 1 < max_x
        top = y > 0
        bottom = y + 1 < max_y

        if left:
            neighbours.append((x - 1, y))
        if right:
            neighbours.append((x + 1, y))
        if top:
            neighbours.append((x, y - 1))
        if bottom:
            neighbours.append((x, y + 1))

        return neighbours

    def __backtrack_path(self, x, y):
        current_distance = self.__wave_grid[x, y]

        if current_distance == 1:
            # reached robot position!
            return [[x, y]]
        elif current_distance < 1:
            print("error current_distance < 1")
            assert error
        elif current_distance > 1:
            next_distance = current_distance - 1

            neighbours = self.__get_neighbours(x, y)

            shortest_neighbour = None

            for neighbour in neighbours:
                value = self.__wave_grid[neighbour[0], neighbour[1]]

                if value == next_distance:
                    shortest_neighbour = neighbour

            path_from_neighbour = self.__backtrack_path(shortest_neighbour[0], shortest_neighbour[1])
            path_from_neighbour.append([x, y])
            # return the recurive call plus append these coords to list
            return path_from_neighbour
