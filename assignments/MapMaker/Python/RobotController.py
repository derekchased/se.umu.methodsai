""" Robot path following implementation based on the Pure Pursuit algorithm """
import math
import sys

import NPFunctions as npf
from Explorer import Explorer
from LaserSensorModel import LaserSensorModel
from OccupancyGrid import OccupancyGrid
from RobotDrive import RobotDrive
from robot import Robot
from show_map import *


class RobotController:
    # Map grid size in meters per square
    MAP_GRID_SIZE = 0.2

    def __init__(self, x_min, y_min, x_max, y_max, show_gui=False, url="http://localhost:50000"):
        self.__robot = Robot(url)
        self.__robot_drive = RobotDrive(self.__robot)

        width_wcs = x_max - x_min
        height_wcs = y_max - y_min
        width_grid = math.ceil(width_wcs / self.MAP_GRID_SIZE)
        height_grid = math.ceil(height_wcs / self.MAP_GRID_SIZE)

        self.__local_map = OccupancyGrid(x_min, y_min, self.MAP_GRID_SIZE, width_grid, height_grid)
        self.__laser = LaserSensorModel(self.__robot, self.__local_map)
        self.__show_map = ShowMap(width_grid, height_grid, show_gui)

        self.__explorer = Explorer(self.__robot, self.__local_map)

        self.__loop_running = False
        self.__take_a_scan = False
        self.__determine_frontiers = False


    def main(self):

        # arbitrary coordinates
        robot_wcs = npf.conv_pos_to_np(self.__robot.getPosition())
        self.__robot_drive.add_coordinate(robot_wcs[0]-2, robot_wcs[0]+2)
        #self.__robot_drive.add_coordinate(3, 20)
        #self.__robot_drive.add_coordinate(22, 1)
        
        self.__loop_running = True
        self.__robot_drive.start_robot()

        self.main_loop()

    def main_loop(self):
        while self.__loop_running:
            if self.__take_a_scan:
                self.__robot.setMotion(0.0, 0.0)
                self.take_scan()
                self.update_map()
                self.__take_a_scan = False
            if self.__determine_frontiers:
                frontiers = self.__explorer.get_frontiers()

                # TODO
                # navigator.navigate_to(frontiers[0]) ?
            if self.__robot_drive.get_running_status():
                self.__robot_drive.take_step()
            else:
                self.__robot.setMotion(0.0, 0.0)
            time.sleep(.1)

        self.end_program()

    def end_program(self):
        self.__show_map.close()

    def take_scan(self):
        self.__laser.update_grid()

    def update_map(self):
        # Get robot XY position
        position_wcs = self.__robot.getPosition()

        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__local_map.pos_to_grid(position_wcs['X'], position_wcs['Y'])

        # Update map with latest grid values and the robot's position
        self.__show_map.updateMap(self.__local_map.get_grid(), 1, robot_x_grid, robot_y_grid)



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
        x_min = y_min = -40
        x_max = y_max = 40

        # TODO: exit(1)

    robotController = RobotController(x_min, y_min, x_max, y_max, show_gui, url)
    robotController.main()
