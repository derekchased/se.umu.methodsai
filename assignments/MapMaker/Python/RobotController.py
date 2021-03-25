""" Robot path following implementation based on the Pure Pursuit algorithm """
import math
import sys

import NPFunctions as npf
from Explorer import Explorer
from LaserSensorModel import LaserSensorModel
from OccupancyGrid import OccupancyGrid
from RobotDrive import RobotDrive
from WavefrontPlanner import WavefrontPlanner
from robot import Robot
from show_map import *


class RobotController:
    # Map grid size in meters per square
    MAP_GRID_SIZE = .2

    # Keep track of number of steps taken in the main_loop
    CYCLES = 0

    def __init__(self, x_min, y_min, x_max, y_max, show_gui=False, url="http://localhost:50000"):
        self.__robot = Robot(url)
        self.__robot_drive = RobotDrive(self.__robot)

        width_wcs = x_max - x_min
        height_wcs = y_max - y_min
        width_grid = math.ceil(width_wcs / self.MAP_GRID_SIZE)
        height_grid = math.ceil(height_wcs / self.MAP_GRID_SIZE)

        self.__local_map = OccupancyGrid(x_min, y_min, self.MAP_GRID_SIZE, height_grid, width_grid)
        self.__laser = LaserSensorModel(self.__robot, self.__local_map)
        self.__show_map = ShowMap(height_grid, width_grid, show_gui)
        self.__explorer = Explorer(self.__robot, self.__local_map)
        self.__path_planner = WavefrontPlanner(self.__robot, self.__local_map, self.__explorer)
        self.__loop_running = False
        self.__take_a_scan = False
        self.__determine_frontiers = False

    def main(self):
        self.__loop_running = True
        self.__take_a_scan = True
        self.__determine_frontiers = False
        self.main_loop()

    def main_loop(self):

        while self.__loop_running:
            
            # Force take a scan every 10 cycles
            if self.CYCLES % 10 == 0:
                self.__take_a_scan = True

            # Update map if scan flag is true
            if self.__take_a_scan:
                self.__robot.setMotion(0.0, 0.0)
        
                self.__laser.update_grid()

                # Get robot XY position
                position_wcs = self.__robot.getPosition()

                # Calculate the robot's position on the grid.
                robot_x_grid, robot_y_grid = self.__local_map.wcs_to_grid(position_wcs['X'], position_wcs['Y'])

                # Update map with latest grid values and the robot's position
                self.__show_map.updateMap(self.__local_map.get_grid(), 1, robot_x_grid, robot_y_grid)

                self.__show_map.close()

                self.__take_a_scan = False

            # Update frontier nodes
            if self.__determine_frontiers:

                frontiers = []#self.__explorer.get_frontiers()

                
                if len(frontiers) > 0:

                    # TODO, frontier should be some minimum distance away from the robot

                    # TODO, which node to select?
                    #  -> for now, take furthest node
                    frontier_x_grid = int(frontiers[-1][0])
                    frontier_y_grid = int(frontiers[-1][1])
                    
                    # add/update green dot on the image
                    self.__show_map.set_frontier(frontier_x_grid, frontier_y_grid)
                    
                    # Get new path from the path planner
                    path_grid = np.array(self.__path_planner.get_grid_path(frontier_x_grid, frontier_y_grid))

                    # Convert path (grid) to WCS
                    path_x_wcs, path_y_wcs = self.__local_map.grid_to_wcs(path_grid[:,0],path_grid[:,1])
                    path_wcs = np.zeros((len(path_x_wcs), 2))
                    path_wcs[:,0] = path_x_wcs
                    path_wcs[:,1] = path_y_wcs

                    # Give WCS path to robot drive
                    self.__robot_drive.set_WCS_path(np.array(path_wcs))
                    
                    # Close flag
                    self.__determine_frontiers = False

                #else:
                    ## TODO what to do when no frontier nodes are returned
                    #assert error
                #frontiers = []#self.__explorer.get_frontiers()

                # bottom right
                #self.__robot_drive.add_wcs_coordinate(*self.__local_map.grid_to_wcs(150, 150))

                # ? maybe bttom left
                #self.__robot_drive.add_wcs_coordinate(*self.__local_map.grid_to_wcs(0, 150))

                # top right
                #self.__robot_drive.add_wcs_coordinate(*self.__local_map.grid_to_wcs(150, 0))

                # top left
                self.__robot_drive.add_wcs_coordinate(*self.__local_map.grid_to_wcs(0, 0))
                    
                # Close flag
                self.__determine_frontiers = False

            # If robot has a point to navigate to, take next step
            if self.__robot_drive.has_navigation_point():
                self.__robot_drive.take_step()
            
            # If no navigation point, determine new frontier nodes
            if not self.__robot_drive.has_navigation_point():
                self.__determine_frontiers = True
                self.__robot.setMotion(0.0, 0.0)

            # Keep track of total cycles
            self.CYCLES += 1

            # Wait before next cycle
            time.sleep(.1)

        # If broken out of the loop then end the program
        self.__show_map.close()


if __name__ == "__main__":
    arguments = sys.argv

    programname = arguments[0]

    try:
        url = arguments[1]
        x_min = int(arguments[2])
        y_min = int(arguments[3])
        x_max = int(arguments[4])
        y_max = int(arguments[5])
        show_gui = int(arguments[6]) == 0
    except:
        print("Usage:", programname, "<url> <x_min> <y_min> <x_max> <y_max> <showGUI>")
        print("Using defaults.")

        url = "http://localhost:50000"
        show_gui = False
        x_min = y_min = -20
        x_max = y_max = 20

        # TODO: exit(1)

    robotController = RobotController(x_min, y_min, x_max, y_max, show_gui, url)
    robotController.main()
