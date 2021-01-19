""" Robot path following implementation based on the Pure Pursuit algorithm """

from Robot import *
from Path import *
from ShowPath import *
import matplotlib.pyplot as plt
import numpy as np
import NPFunctions as npf
from RobotDrive import RobotDrive

class RobotController:

    # Constructor, takes path filename
    def __init__(self, path_name):
        self._robot = Robot()

        # Create path and convert from json to numpy matrix
        p = Path(path_name)
        self._path = p.getPath()
        self._path_matrix = npf.conv_path_to_np(self._path)

        # Show path to user
        self._sp = ShowPath(self._path)

        # Create Driving Module
        self._robot_drive = RobotDrive(self._robot, self._path_matrix, self._sp)

        
        


    def start_robot(self):
        # Start robot driving
        self._robot_drive.start_robot()
        self._robot_drive.drive_robot()

    def stop_robot(self):
        self._robot_drive.stop_robot()
        self._sp.pause_the_plot()



if __name__ == "__main__":
    # Available paths:
    # Path-around-table-and-back.json
    # Path-around-table.json
    # Path-to-bed.json
    # Path-from-bed.json
    # Filename of the path is passed in through the command line argument
    # robotController = RobotController(sys.argv[1])
    robotController = RobotController("Path-around-table-and-back.json")
    robotController.start_robot()
