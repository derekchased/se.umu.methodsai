#!/usr/bin/python3
from Robot import *
from Path import *
from ShowPath import *
import math

# load a path file
p = Path("exam2020.json")
path = p.getPath()

# plot the path
sp = ShowPath(path)

print("Path length = " + str(len(path)))
print("First point = " + str(path[0]['X']) + ", " + str(path[0]['Y']))

# make a robot to move around
robot = Robot()


def unpackPosition(position):
    return [position['X'], position['Y']]


def xyDistance(x1, y1, x2, y2):
    """
    Calculates the Euclidian distance between (x1, y1) and (x2, y2).
    """
    deltaX = abs(x1 - x2)
    deltaY = abs(y1 - y2)

    return math.sqrt(deltaX * deltaX + deltaY * deltaY)


def findClosestPointOnPath(robot, path, previousPointIdx, maxLookahead):
    """
    Finds the point on the path that is closest to the robot.
    :param robot:               A Robot object
    :param path:                A list of path points, as returned by Path.getPath()
    :param previousPointIdx:    The index of the previous path point.
    :param maxLookahead:        The maximum amount of path points to look forward to find the next closest path point
    :return:                    The index of the path point closest to the robot.
    """
    x, y = unpackPosition(robot.getPosition())

    closestPoint = 0
    closestDistance = math.inf

    for idx in range(previousClosestPoint, len(path)):
        pathX, pathY = unpackPosition(path[idx])
        distance = xyDistance(x, y, pathX, pathY)

        # Don't look more than maxLookahead points ahead on the path.
        if idx - previousPointIdx > maxLookahead:
            break

        if distance < closestDistance:
            closestDistance = distance
            closestPoint = idx
    return closestPoint


def findLookaheadPoint(path, closestPoint, lookAheadDistance):
    """
    Find the lookahead point on a path. The lookahead point is a point on the path that is at least
    `lookAheadDistance` meters from the point on the path that is closest to the robot.

    :param path:                A list of path points, as given by Path.getPath()
    :param closestPoint:        The index of the path point that is closest to the robot
    :param lookAheadDistance:   The lookahead distance in meters.
    :return:                    The index of the lookahead point
    """
    x, y = unpackPosition(path[closestPoint])

    for idx in range(closestPoint + 1, len(path)):
        pathX, pathY = unpackPosition(path[idx])
        distance = xyDistance(x, y, pathX, pathY)

        if (distance >= lookAheadDistance):
            return path[idx]
    return path[len(path) - 1]


def getOrientationError(robot, lookaheadPoint):
    """
    Return the orientation error in radians

    :param robot:           A Robot object
    :param lookaheadPoint:  A path point that is the lookahead point
    :return:                The orientation error in radians
    """
    xR, yR = unpackPosition(robot.getPosition())
    xP, yP = unpackPosition(lookaheadPoint)
    correctOrientation = math.atan2(yP - yR, xP - xR)

    er = correctOrientation - robot.getHeading()

    # Correct error to be in range [-pi, pi)
    while er <= -math.pi:
        er = er + math.pi * 2
    while er > math.pi:
        er = er - math.pi * 2

    return er


maxspeed = 0.4
k = .9
lookaheadDistance = .3

goalX, goalY = unpackPosition(path[-1])

try:
    previousClosestPoint = 0

    while True:
        time.sleep(0.1)

        closestPoint = findClosestPointOnPath(robot, path, previousClosestPoint, 100)
        lookAheadPoint = findLookaheadPoint(path, closestPoint, lookaheadDistance)

        orientationError = getOrientationError(robot, lookAheadPoint)

        # adjust robot speed based on orientation error, this makes
        # it slow down on tight curves or when far from the path
        speed = maxspeed - abs(orientationError) * 0.4

        # Control the robots speed
        robot.setMotion(speed, orientationError * k)

        # print a bunch of numbers
        print("Speed", speed)
        print("Closest point ", closestPoint)
        print("lookahead Point")
        print(lookAheadPoint)
        print("pos, heading")
        print(robot.getPosition())
        print(robot.getHeading())
        print(orientationError)

        # Plot the current position and the look-ahead point:
        sp.update(robot.getPosition(), unpackPosition(lookAheadPoint))

        # stop the program if the robot is within 10 cm from the goal
        rX, rY = unpackPosition(robot.getPosition())
        goalDistance = xyDistance(goalX, goalY, rX, rY)

        print("Distance to goal", goalDistance)

        if goalDistance < .1:
            break

        previousClosestPoint = closestPoint
except:
    robot.setMotion(0, 0)

# echoes = robot.getLaser()
# print(echoes)

robot.setMotion(0, 0)
