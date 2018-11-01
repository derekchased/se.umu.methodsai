#!/usr/bin/env python3
"""
Example demonstrating how to communicate with Microsoft Robotic Developer
Studio 4 via the Lokarria http interface. 

Author: Erik Billing (billing@cs.umu.se)

Updated by Ola Ringdahl 2014-09-11
Updated by Lennart Jern 2016-09-06 (converted to Python 3)
Updated by Filip Allberg and Daniel Harr 2017-08-30 (actually converted to Python 3)
Updated by Ola Ringdahl 2017-10-18 (added example code that use showMap)
Updated by Ola Ringdahl 2018-11-01 (fixed so that you can write the address with http://
    without getting a socket error. Added a function for converting (x,y) to (row,col))
"""

url = 'http://localhost:50000'
# HTTPConnection does not want to have http:// in the address apparently, so lest's remove it:
MRDS_URL = url[len("http://"):]

import http.client, json, time
import numpy as np
from math import sin, cos, pi, atan2
from show_map import ShowMap

HEADERS = {"Content-type": "application/json", "Accept": "text/json"}


class UnexpectedResponse(Exception):
    pass


def postSpeed(angularSpeed, linearSpeed):
    """Sends a speed command to the MRDS server"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    params = json.dumps({'TargetAngularSpeed': angularSpeed, 'TargetLinearSpeed': linearSpeed})
    mrds.request('POST', '/lokarria/differentialdrive', params, HEADERS)
    response = mrds.getresponse()
    status = response.status
    # response.close()
    if status == 204:
        return response
    else:
        raise UnexpectedResponse(response)


def getLaser():
    """Requests the current laser scan from the MRDS server and parses it into a dict"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    mrds.request('GET', '/lokarria/laser/echoes')
    response = mrds.getresponse()
    if response.status == 200:
        laserData = response.read()
        response.close()
        return json.loads(laserData.decode())
    else:
        return response


def getLaserAngles():
    """Requests the current laser properties from the MRDS server and parses it into a dict"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    mrds.request('GET', '/lokarria/laser/properties')
    response = mrds.getresponse()
    if response.status == 200:
        laserData = response.read()
        response.close()
        properties = json.loads(laserData.decode())
        beamCount = int((properties['EndAngle'] - properties['StartAngle']) / properties['AngleIncrement'])
        a = properties['StartAngle']  # +properties['AngleIncrement']
        angles = []
        while a <= properties['EndAngle']:
            angles.append(a)
            a += pi / 180  # properties['AngleIncrement']
        # angles.append(properties['EndAngle']-properties['AngleIncrement']/2)
        return angles
    else:
        raise UnexpectedResponse(response)


def getPose():
    """Reads the current position and orientation from the MRDS"""
    mrds = http.client.HTTPConnection(MRDS_URL)
    mrds.request('GET', '/lokarria/localization')
    response = mrds.getresponse()
    if response.status == 200:
        poseData = response.read()
        response.close()
        return json.loads(poseData.decode())
    else:
        return UnexpectedResponse(response)


def getHeading():
    """Returns the XY Orientation as a heading unit vector"""
    return heading(getPose()['Pose']['Orientation'])


def createMap():
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
    pose = getPose()
    curr_pos = pose['Pose']['Position']
    robot_coord = pos_to_grid(curr_pos['X'], curr_pos['Y'], min_x, max_y, cell_size)
    robot_row = robot_coord[0]
    robot_col = robot_coord[1]

    # Update the map
    map.updateMap(grid, maxVal, robot_row, robot_col)
    print("Map updated")

    time.sleep(2)
    # Let's update the map again. You should update the grid and the position
    # In your solution you should not sleep of course, but update continuously
    pose = getPose()
    curr_pos = pose['Pose']['Position']
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


def heading(q):
    return rotate(q, {'X': 1.0, 'Y': 0.0, "Z": 0.0})


def rotate(q, v):
    return vector(qmult(qmult(q, quaternion(v)), conjugate(q)))


def quaternion(v):
    q = v.copy()
    q['W'] = 0.0
    return q


def vector(q):
    v = {}
    v["X"] = q["X"]
    v["Y"] = q["Y"]
    v["Z"] = q["Z"]
    return v


def conjugate(q):
    qc = q.copy()
    qc["X"] = -q["X"]
    qc["Y"] = -q["Y"]
    qc["Z"] = -q["Z"]
    return qc


def qmult(q1, q2):
    q = {}
    q["W"] = q1["W"] * q2["W"] - q1["X"] * q2["X"] - q1["Y"] * q2["Y"] - q1["Z"] * q2["Z"]
    q["X"] = q1["W"] * q2["X"] + q1["X"] * q2["W"] + q1["Y"] * q2["Z"] - q1["Z"] * q2["Y"]
    q["Y"] = q1["W"] * q2["Y"] - q1["X"] * q2["Z"] + q1["Y"] * q2["W"] + q1["Z"] * q2["X"]
    q["Z"] = q1["W"] * q2["Z"] + q1["X"] * q2["Y"] - q1["Y"] * q2["X"] + q1["Z"] * q2["W"]
    return q


if __name__ == '__main__':
    print('Sending commands to MRDS server', MRDS_URL)
    try:
        print('Telling the robot to go straight ahead.')
        response = postSpeed(0, 0.5)
        createMap()
        print('Waiting for a while...')
        time.sleep(3)
        print('Telling the robot to go in a circle.')
        response = postSpeed(0.9, 0.1)
    except UnexpectedResponse as ex:
        print('Unexpected response from server when sending speed commands:', ex)

    try:
        laser = getLaser()
        laserAngles = getLaserAngles()
        print(
            'The rightmost laser beam has angle %.3f deg from x-axis (straight forward) and distance %.3f '
            'meters.createMap' % (
                laserAngles[0], laser['Echoes'][0]
            ))
        print('Beam 1: %.3f Beam 269: %.3f Beam 270: %.3f' % (
            laserAngles[0] * 180 / pi, laserAngles[269] * 180 / pi, laserAngles[270] * 180 / pi))
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading laser data:', ex)

    try:
        pose = getPose()
        print('Current position: ', pose['Pose']['Position'])
        print('------- Laser values ------')
        for t in range(10):
            print('Current heading vector: X:{X:.3}, Y:{Y:.3}'.format(**getHeading()))
            laser = getLaser()
            print('Distance %.3f meters.' % (laser['Echoes'][135]))
            if laser['Echoes'][135] < 0.3:
                print('Danger! Brace for impact! Hit the brakes!')
                response = postSpeed(0, -0.1)
            time.sleep(1)
        postSpeed(0, 0)
        print("I'm done here!")
    except UnexpectedResponse as ex:
        print('Unexpected response from server when reading position:', ex)
