
from robot import Robot
from OccupancyGrid import OccupancyGrid
from Explorer import Explorer
import numpy as np

class WavefrontPlanner:

    OPEN_CERTAINTY = .54

    def __init__(self, robot: Robot, occupancy_grid: OccupancyGrid, explorer:Explorer):
        self.__robot = robot
        self.__occupancy_grid = occupancy_grid
        self.__cols, self.__rows = self.__occupancy_grid.get_size()
        self.__explorer = explorer
        self.__wave_grid = []
        


    def get_grid_path(self, frontier_x_grid:int, frontier_y_grid:int):
        # Get robot XY position
        position_wcs = self.__robot.getPosition()

        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__occupancy_grid.pos_to_grid(position_wcs['X'], position_wcs['Y'])
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
            current_wave_coordinates = np.transpose((self.__wave_grid==current_distance).nonzero())

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
                assert error
            else:
                goal_point_value = self.__wave_grid[frontier_x_grid, frontier_y_grid]
                if goal_point_value < 0:
                    expand_wave = False
                elif goal_point_value > 0:
                    expand_wave = False

        if goal_point_value < 0:
            print("goal_point_value < 0 (marked as obstacle)", current_distance)
            # TODO- goal poiint marked as an obstacle
            # select closest? choose different fronteir node?
            assert error
        elif goal_point_value == 0:
            # TODO- goal point was not reached (perhaps surrounded by obstacles)
            # select closest? choose different fronteir node?
            print("goal_point_value == 0 (not checked yet)", current_distance)
            assert error
        else:
            # TODO- goal point reached
            back_list = self.__backtrack_path(int(frontier_x_grid), int(frontier_y_grid))
            #print(goal_point_value, "path", back_list)
            return back_list

    def __update_neighbors(self, x, y, distance):
        # keep list of neighbors that get updated
        updated_neighbors = []

        #up
        if y-1 >= 0 and self.__wave_grid[x, y-1] == 0:
            if self.__occupancy_grid.get_grid()[x, y-1] < self.OPEN_CERTAINTY:
                self.__wave_grid[x, y-1] = distance
                updated_neighbors.append((x, y-1))
            else:
                self.__wave_grid[x, y-1] = -1

        #left
        if x-1 >= 0 and self.__wave_grid[x-1, y] == 0:
            if self.__occupancy_grid.get_grid()[x-1, y] < self.OPEN_CERTAINTY:
                self.__wave_grid[x-1, y] = distance
                updated_neighbors.append((x-1, y))
            else:
                self.__wave_grid[x-1, y] = -1
        #right
        if x+1 < self.__cols and self.__wave_grid[x+1, y] == 0:
            if self.__occupancy_grid.get_grid()[x+1, y] < self.OPEN_CERTAINTY:
                self.__wave_grid[x+1, y] = distance
                updated_neighbors.append((x+1, y))
            else: 
                self.__wave_grid[x+1, y] = -1

        #down
        if y+1 < self.__rows and self.__wave_grid[x, y+1] == 0:
            if self.__occupancy_grid.get_grid()[x, y+1] < self.OPEN_CERTAINTY:
                updated_neighbors.append((x, y+1))
                self.__wave_grid[x, y+1] = distance
            else:
                self.__wave_grid[x, y+1] = -1

        return updated_neighbors

    def __backtrack_path(self, x, y):
        current_goal_point_value = self.__wave_grid[x, y]

        if current_goal_point_value == 1:
            # append the robot's starting position
            return [[x, y]]
        elif current_goal_point_value < 1:
            # TODO some error
            print("error current_goal_point_value < 1")
            assert error
            return []
        elif current_goal_point_value > 1:
            next_value = current_goal_point_value-1

            # up
            if y-1 >= 0 and self.__wave_grid[x, y-1] == next_value:
                next_x = x
                next_y = y-1

            #left
            elif x-1 >= 0 and self.__wave_grid[x-1, y] == next_value:
                next_x = x-1
                next_y = y

            #right
            elif x+1 < self.__cols and self.__wave_grid[x+1, y] == next_value:
                next_x = x+1
                next_y = y

            #down
            elif y+1 < self.__rows and self.__wave_grid[x, y+1] == next_value:
                next_x = x
                next_y = y+1


            ret_list = self.__backtrack_path(next_x, next_y)
            ret_list.append([x,y])
            # return the recurive call plus append these coords to list
            return ret_list
