""" Robot path following implementation based on the Pure Pursuit algorithm """

import sys
import time
import math
import numpy as np
import NPFunctions as npf

LOOK_AHEAD_DISTANCE = 5
GOAL_THRESHOLD = .5
MAX_LINEAR_SPEED = 1

class RobotDrive:

    # Constructor, takes path filename
    def __init__(self, robot):
        self.__robot = robot
        self.__has_navigation = False

    def add_wcs_coordinate(self, wcs_x, wcs_y, wcs_z=0):
        """
        Sets a single coordinate for the robot to navigate to
        
        Args:
            wcs_x (float): x position
            wcs_y (float): y position
            wcs_z (float, optional): z position (not used by robot i think??)
        """
        try:
            self._path_matrix = np.append(self._path_matrix,np.array([wcs_x, wcs_y,wcs_z]).reshape(1,3),axis=0)
        except:
            self._path_matrix = np.array([wcs_x, wcs_y,wcs_z]).reshape(1,3)
        
        self.__has_navigation = True
        
    def set_WCS_path(self, path_matrix):
        """
        Sets a series of coordinates along a path for the robot to navigate through
        
        Args:
            path_matrix (numpy): a matrix of coordinates [ (x, y, z), (x, y, z), ...]
        """

        # if missing z index, add a column of zeros to the end
        shape = path_matrix.shape
        if shape[1] < 3:
            path_matrix_z = np.zeros((shape[0],shape[1]+1))
            path_matrix_z[:,:-1] = path_matrix
            path_matrix = path_matrix_z
        self._path_matrix = path_matrix

        # Set flag to true
        self.__has_navigation = True

    def has_navigation_point(self):
        return self.__has_navigation

    # Main method to determine and update robot's velocity and heading
    def take_step(self):
        if not self.__has_navigation:
            print("no navigation point")
            return
                
        self.__robot_position = self.__robot.getPosition()

        # Convert robot's position to a numpy array
        self.__robot_position_vector = npf.conv_pos_to_np(self.__robot_position)

        # Get distances from robot to each point
        self.__robot_to_path_distances = npf.compute_distances_vector_matrix(self.__robot_position_vector, self._path_matrix)

        # Find furthest valid point
        goal_point_index = self._find_goal_point_index()

        print("distance to nav point"+str(goal_point_index)+":",self.__robot_to_path_distances[goal_point_index])

        # Get goal point as vector
        self._goal_point_coordinate_world = self._path_matrix[goal_point_index]

        # Get goal point x and y
        goal_point_x_WCS = self._goal_point_coordinate_world[0]
        goal_point_y_WCS = self._goal_point_coordinate_world[1]

        # Get robot's global x and y coordinate
        robot_position_x_WCS = self.__robot_position_vector[0]
        robot_position_y_WCS = self.__robot_position_vector[1]

        # Get robot's current heading
        psi = self.__robot.getHeading()

        # Convert goal point in world coordinates to robot's local coordinates
        goal_point_x_RCS =  (goal_point_x_WCS - robot_position_x_WCS) * math.cos(psi) + (goal_point_y_WCS - robot_position_y_WCS) * math.sin(psi)
        goal_point_y_RCS = -(goal_point_x_WCS - robot_position_x_WCS) * math.sin(psi) + (goal_point_y_WCS - robot_position_y_WCS) * math.cos(psi)

        # Get robot local heading towards goal point
        gp_angle_RCS = math.atan2(goal_point_y_RCS, goal_point_x_RCS)

        # Get heading in local degrees
        gp_abs_angle_RCS_degree = abs(gp_angle_RCS) * 180 / math.pi

        # Choose linear speed based on degree of turning angle (tighter angle, slower speed)
        linear_speed = 5

        # Calculate turn rate
        g = 2 * goal_point_y_RCS / LOOK_AHEAD_DISTANCE**2
        turn_rate = linear_speed * g
        if turn_rate >= .1:  
            linear_speed = 25

        # Update robot speed and turn rate
        self.__robot.setMotion(linear_speed, turn_rate/2)

        # Shorten the path matrix
        self._path_matrix = self._path_matrix[goal_point_index:,:]

#        print("takestep",self.__robot_to_path_distances[0])
        
        # Determine if robot has anywhere to go
        if (len(self._path_matrix) == 1 and self.__robot_to_path_distances[0] < GOAL_THRESHOLD):
            self.__has_navigation = False
            self._path_matrix = None
            self.__robot.setMotion(0, 0)

    def _find_goal_point_index(self):

        # initialize to first point in the path
        goal_point_index = 0

        # iterate through points along the path, from first to last
        # if a point is <= look ahead distance, choose as next point
        # if a point is > look ahead distance break out of loop and return the index
        for i, j in enumerate(self.__robot_to_path_distances):
            if j <= LOOK_AHEAD_DISTANCE:
                goal_point_index = i
            else:
                break
        return goal_point_index
