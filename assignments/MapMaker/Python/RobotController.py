""" Robot path following implementation based on the Pure Pursuit algorithm """
from LaserSensorModel import LaserSensorModel
from OccupancyGrid import OccupancyGrid
from robot import Robot
from show_map import *


class RobotController:

    # Constructor, takes path filename
    def __init__(self):
        self.__robot = Robot()

        self.__local_map = OccupancyGrid(-20, -20, 0.2, 200, 200)
        self.__laser = LaserSensorModel(self.__robot, self.__local_map)
        self.__show_map = ShowMap(200, 200, False)


    def start_robot(self):
        stop_time = time.time() + 3

        # self.__laser.update_grid()
        while time.time() < stop_time:
            self.__laser.update_grid()

            time.sleep(0.1)

        # Get robot XY position
        position_wcs = self.__robot.getPosition()
        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__local_map.pos_to_grid(position_wcs['X'], position_wcs['Y'])
        self.__show_map.updateMap(self.__local_map.get_grid(), 1, robot_x_grid, robot_y_grid)
        self.__show_map.close()


    def stop_robot(self):
        pass



if __name__ == "__main__":
    robotController = RobotController()
    robotController.start_robot()
