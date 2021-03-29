from robot import Robot


class ObstacleAvoider:

    def __init__(self, robot: Robot):
        self.__robot = robot


    def in_danger(self):
        """
        Returns true if the robot is in danger of colliding with an obstacle.
        If this has been set to true, path planning and frontier detection should reoccur.
        """

        # Read laser sensor

        # If too close, return true

        return False

    def loop(self):
        """
        If `in_danger` returns True, this function gets complete control of the robot until the robot is not in danger
        anymore.
        """

        # Move in such a way that the in_danger is not firing anymore.