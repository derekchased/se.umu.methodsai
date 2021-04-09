""" Robot path following implementation based on the Pure Pursuit algorithm """
import math
import sys
import traceback

import NPFunctions as npf
from Explorer import Explorer
from LaserSensorModel import LaserSensorModel
from ObstacleAvoider import ObstacleAvoider
from OccupancyGrid import OccupancyGrid
from RobotDrive import RobotDrive
from WavefrontPlanner import WavefrontPlanner
from robot import Robot
from show_map import *


class RobotController:
    
    def __init__(self, x_min, y_min, x_max, y_max, show_gui=False, url="http://localhost:50000"):
        self.__robot = Robot(url)
        self.__robot_drive = RobotDrive(self.__robot)

        # Map grid size in meters per square (robot is 450 x 400 x 243 (LxWxH))
        MAP_GRID_SIZE = .2

        # Set coordinates and dimensions of local map area within the world coordinate system
        width_wcs = x_max - x_min
        height_wcs = y_max - y_min
        width_grid = math.ceil(width_wcs / MAP_GRID_SIZE)
        height_grid = math.ceil(height_wcs / MAP_GRID_SIZE)

        self.__local_map = OccupancyGrid(x_min, y_min, MAP_GRID_SIZE, height_grid, width_grid)
        self.__laser = LaserSensorModel(self.__robot, self.__local_map)
        self.__show_map = ShowMap(height_grid, width_grid, show_gui)
        self.__explorer = Explorer(self.__robot, self.__local_map)
        self.__path_planner = WavefrontPlanner(self.__robot, self.__local_map)
        self.__obstacle_avoider = ObstacleAvoider(self.__robot, self.__local_map)
        
        # Keep track of number of steps taken in the main_loop
        self.__SCAN_FREQUENCY = 10
        self.__cycles = 0
        self.__loop_running = False
        self.__take_a_scan = False
        self.__determine_frontiers = False
        self.__in_reactive_state = False

    def main(self):

        # Start program
        self.__loop_running = True
        self.__take_a_scan = True
        self.__determine_frontiers = True

        try:
            self.main_loop()
        except KeyboardInterrupt:
            self.__robot.setMotion(0, 0)

    def main_loop(self):
        while self.__loop_running:
            # Force take a scan 
            if self.__cycles % self.__SCAN_FREQUENCY == 0:
                self.__take_a_scan = True

            # Update map if scan flag is true
            if self.__take_a_scan:
                self.__do_take_scan()

            # Update frontier nodes
            if self.__determine_frontiers:
                self.__do_determine_frontiers()

            # If robot has a point to navigate to, take next step
            if self.__robot_drive.has_navigation_point():
                self.__robot_drive.take_step()

            # If no navigation point, determine new frontier nodes
            if not self.__robot_drive.has_navigation_point():
                self.__determine_frontiers = True
                self.__robot.setMotion(0.0, 0.0)

            in_danger, in_warning = self.__obstacle_avoider.in_danger()
            
            self.__robot_drive.warning(in_warning)

            if in_danger:
                self.reactive_loop()

            # Keep track of total cycles
            self.__cycles += 1

            # Wait before next cycle
            time.sleep(.1)

        # If broken out of the loop then end the program
        self.__show_map.close()

    def reactive_loop(self):
        print("R: start reactive_loop")

        # Stop motion to avoid potential collision
        self.__robot.setMotion(0.0, 0.0)
        
        # Find new frontier
        self.__do_determine_frontiers()
        
        # Enter reactive mode, essentially disabling further obstacle detection, assume
        # the robot can get out of this dangerous situation. End the loop and return when
        # robot is no longer in danger
        while self.__obstacle_avoider.in_danger():
            
            print("R: has_navigation_point()", self.__robot_drive.has_navigation_point())
            if self.__robot_drive.has_navigation_point():

                self.__robot_drive.take_step()

            else:

                # Robot was given a point to reach but could not.
                # if you scan for a new frontier from here, this
                # could start an infinite loop of nothingness
                raise Exception("Reactive loop error")

            
            self.__cycles += 1

            if self.__cycles % self.__SCAN_FREQUENCY == 0:

                self.__take_a_scan = True
            
            time.sleep(.1)


        self.__robot.setMotion(0.0, 0.0)
        self.__take_a_scan = True
        self.__determine_frontiers = True

        print("R: end reactive_loop")

    def __do_take_scan(self):
        #print("Taking scan")
        
        # Get robot position
        position_wcs = self.__robot.getPosition()
        heading = self.__robot.getHeading()
        self.__laser.update_grid(position_wcs['X'], position_wcs['Y'])

        # Calculate the robot's position on the grid.
        robot_col, robot_row = self.__local_map.wcs_to_grid(position_wcs['X'], position_wcs['Y'])

        # Update map with latest grid values and the robot's position
        self.__show_map.updateMap(self.__local_map.get_grid(), robot_col, robot_row, heading)

        self.__show_map.close()

        self.__take_a_scan = False

    def __do_determine_frontiers(self):
        frontiers = self.__explorer.get_frontiers()

        if len(frontiers) > 0:
            # add/update green dots on the image
            self.__show_map.set_frontiers(frontiers)

            # Get new path from the path planner
            path, frontier_x, frontier_y = self.__path_planner.get_path_to_frontier(frontiers)
            
            path_grid = np.array(path)

            print("next frontier:", frontier_x, frontier_y, "len(path_grid):",len(path_grid))

            # Convert path (grid) to WCS
            path_x_wcs, path_y_wcs = self.__local_map.grid_to_wcs(path_grid[:, 0], path_grid[:, 1])
            path_wcs = np.zeros((len(path_x_wcs), 2))
            path_wcs[:, 0] = path_x_wcs
            path_wcs[:, 1] = path_y_wcs

            # Give WCS path to robot drive
            self.__robot_drive.set_WCS_path(np.array(path_wcs))

            self.__show_map.set_path(path_grid)

            # Close flag
            self.__determine_frontiers = False

        else:
            ## TODO what to do when no frontier nodes are returned
            raise Exception("no frontier nodes found")

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
        x_min = -30
        y_min = -30
        x_max = 20
        y_max = 20

        # TODO: exit(1)

    robotController = RobotController(x_min, y_min, x_max, y_max, show_gui, url)

    print("Starting RobotController")

    robotController.main()

    print("Done")
