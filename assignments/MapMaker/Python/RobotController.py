""" Robot path following implementation based on the Pure Pursuit algorithm """
from LaserSensorModel import LaserSensorModel
from OccupancyGrid import OccupancyGrid
from robot import Robot
from show_map import *
import show_map as SM
import matplotlib.pyplot as plt
from RobotDrive import RobotDrive
import NPFunctions as npf

class RobotController:

    # Constructor, takes path filename
    def __init__(self):
        self.__robot = Robot()
        self.__robot_drive = RobotDrive(self.__robot)
        self.__local_map = OccupancyGrid(-20, -20, 0.2, 200, 200)
        self.__laser = LaserSensorModel(self.__robot, self.__local_map)
        self.__show_map = ShowMap(200, 200, False)

    def main(self):

        # Start the robot moving to a random location
        self.take_step()

        # Arbitrary amt of time
        stop_time = time.time() + 10

        # Moved everything into this main for loop because
        # we can't really use the sleep() function in multiple classes
        # we can consider threading or some other implementation
        while time.time() < stop_time:
            self.take_scan()

            # again here, have to call drive on the robot directly
            # because we can't use multiple sleep() functions
            # it breaks control flow
            self.__robot_drive.take_step()
            time.sleep(0.1)

        self.__show_map.close()
        self.__robot_drive.stop_robot()
        self.__robot.setMotion(0.0, 0.0)


    def take_scan(self):
        print("take scan")
        self.__laser.update_grid()
        
        # Get robot XY position
        position_wcs = self.__robot.getPosition()
        
        # Calculate the robot's position on the grid.
        robot_x_grid, robot_y_grid = self.__local_map.pos_to_grid(position_wcs['X'], position_wcs['Y'])

        # Update map with latest grid values and the robot's position
        self.__show_map.updateMap(self.__local_map.get_grid(), 1, robot_x_grid, robot_y_grid)
        
        # To see progress over time
        SM.saveMap(plt.figure(1), "map"+str(time.time())+".png")


    def take_step(self):
        robot_position_vector = npf.conv_pos_to_np(self.__robot.getPosition())
        self.__robot_drive.set_WCS_coordinates(robot_position_vector[0]-5, robot_position_vector[1]+10)
        self.__robot_drive.start_robot()

if __name__ == "__main__":
    robotController = RobotController()
    robotController.main()
    