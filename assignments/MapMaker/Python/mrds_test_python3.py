# Author Ola Ringdahl, ringdahl@cs.umu.se

from robot import *
from math import pi
from show_map import ShowMap
import numpy as np


def main():
    host = "http://127.0.0.1:50000"

    # make a robot to move around
    robot = Robot(host)

    # move the robot
    robot.setMotion(5 * pi / 180, 0.2)
    # create a new map
    create_map(robot)

    for i in range(10):
        time.sleep(0.5)
        print("Current position (meters): %.2f", robot.getPosition())
        print("Current heading: %.3f deg" % (robot.getHeading() * 180 / pi))

    # get the angle of each laser beam
    laser_angles = robot.getLaserAngles()
    # Get the distances of all laser beams
    laser_scan = robot.getLaser()
    print ('The rightmost laser beam has angle %d deg from x-axis (straight forward) and distance %.2f meters.' % (
        laser_angles[0] * 180 / pi, laser_scan['Echoes'][0]))
    print('Beam 0: %d deg, Beam 269: %d deg, Beam 270: %d deg' % (
        laser_angles[0] * 180 / pi, laser_angles[269] * 180 / pi, laser_angles[270] * 180 / pi))

    print ("------------")
    print ("Laser echoes:")
    print(laser_scan['Echoes'])
    print ("------------")
    # Stop robot
    robot.setMotion(0, 0)
    print("That's all folks!")


def create_map(robot):
    """"A simple example of how to use the ShowMap class """
    showGUI = True  # set this to False if you run in putty 
    # use the same no. of rows and cols in map and grid:
    nRows = 60
    nCols = 65
    # Initialize a ShowMap object. Do this only once!!
    map = ShowMap(nRows, nCols, showGUI)
    # create a grid with all cells set to 7 (unexplored) as numpy matrix:
    grid = np.ones(shape=(nRows, nCols)) * 7
    # or as a two-dimensional array:
    # grid = [[7 for col in range(nCols)] for row in range(nRows)]

    # create some obstacles (black/grey)
    # Upper left side:
    grid[0][0] = 15
    grid[0][1] = 15
    grid[0][2] = 15
    grid[0][3] = 15
    grid[0][4] = 15
    grid[0][5] = 15
    grid[0][6] = 15
    grid[0][7] = 15

    # Lower right side:
    grid[59][64] = 15
    grid[58][64] = 15
    grid[57][64] = 15
    grid[56][64] = 15
    grid[55][64] = 15

    # Lower left side:
    grid[59][0] = 12
    grid[59][1] = 11
    grid[59][2] = 10
    grid[59][3] = 9
    grid[59][4] = 8

    # An explored area (white)
    for rw in range(35, 50):
        for cl in range(32, 55):
            grid[rw][cl] = 0

    # Max grid value
    maxVal = 15

    # Hard coded values for max/min x,y
    min_x = -15
    max_y = 17
    cell_size = 0.5

    # Position of the robot in the grid (red dot)
    curr_pos = robot.getPosition()
    robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
    robot_row = robot_coord[0]
    robot_col = robot_coord[1]

    # Update the map
    map.updateMap(grid, maxVal, robot_row, robot_col)
    print("Map updated")
    map.updateMap(grid, maxVal, robot_row, robot_col)

    time.sleep(2)
    # Let's update the map again. You should update the grid and the position
    # In your solution you should not sleep of course, but update continuously
    curr_pos = robot.getPosition()
    robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
    robot_row = robot_coord[0]
    robot_col = robot_coord[1]
    map.updateMap(grid, maxVal, robot_row, robot_col)
    print("Map updated again")


def pos_to_grid(x, y, xmin, ymax, cellsize):
    """
    Converts an (x,y) positon to a (row,col) coordinate in the grid
    :param x: x-position
    :param y: y-position
    :param xmin: The minimum x-position in the grid
    :param ymax: The maximum y-position in the grid
    :param cellsize: the resolution of the grid
    :return: A tuple with (row,col)
    """
    col = (x - xmin) / cellsize
    row = (ymax - y) / cellsize
    return (row, col)


if __name__ == '__main__':
    main()
