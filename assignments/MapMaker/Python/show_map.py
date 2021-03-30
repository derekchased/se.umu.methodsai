import datetime
import threading
import time

import numpy as np
from PIL import Image

"""
ShowMap creates a Gui for showing the progress of the created map and saves it to file every 5 second
Author Peter Hohnloser

Updated by Ola Ringdahl 2019-01-08 (fixed that the plot window hangs in Windows) 
"""

class ShowMap(object):
    def __init__(self, gridHeight, gridWidth, showGUI):
        """
        Constructor for ShowMap

        Args:
            param gridHeight the height of the grid (no. of rows)
            param gridWidth the width of the grid (no. of columns)
            param ShowGUI if true showing the map
        """
        import matplotlib
        if not showGUI:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        self.saveMapTime = 5.0
        now = datetime.datetime.now()
        self.mapName = 'map-' + now.strftime("%Y%m%d-%H%M%S") + '-'
        self.mapNr = 1
        self.first = True
        self.__robot_size = 6
        self.__size = (gridWidth, gridHeight)

        # create a grayscale image
        data = np.ones(shape=self.__size)
        self.__image = Image.fromarray(data * 0.5 * 255)

        # remove the toolbar from plot
        plt.rcParams['toolbar'] = 'None'

        # using matplotlib to show an image in a subplot
        self.__fig, self.__ax = plt.subplots(1, 1)
        self.__fig.suptitle('Show Map')

        # remove the x and y tick in figure
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])

        # Show image window
        self.__implot = self.__ax.imshow(self.__image)

        plt.show(block=False)
        self.__fig.canvas.draw()
        self.__frontiers = []

        self.start_time = time.time()

        self.__path = []

    def set_frontiers(self, frontiers):
        self.__frontiers = frontiers

    def set_path(self, path):
        self.__path = path

    def updateMap(self, grid, robot_col, robot_row, robot_heading):  # TODO add frontiers parameter
        """
        Creates a new BufferedImage from a grid with integer values between 0 - maxVal,
        where 0 is black and maxVal is white, with a grey scale in between. Negative values are shown as gray.
        Call this Method after you have updated the grid.

        Args:
            param grid is the updated grid (numpy matrix or a two-dimensional array)
            param robot_row is the current position of the robot in grid row
            param robot_col is the current position of the robot in grid column
        """
        new_image = Image.fromarray(np.transpose(1.0 - grid) * 255)

        self.__image.paste(new_image)

        # update the plot withe new image
        self.__ax.clear()
        self.__implot = self.__ax.imshow(self.__image)

        # remove the x and y tick in figure
        self.__ax.set_xticks([])
        self.__ax.set_yticks([])

        if len(self.__path) > 0:
            path_xs, path_ys = np.transpose(self.__path)
            self.__ax.scatter(path_xs, path_ys, 1, c='b')

        if len(self.__frontiers) > 0:
            xs, ys = np.transpose(self.__frontiers)
            self.__ax.scatter(xs, ys, 1, c='g')

        heading_col = robot_col + (10 * np.sin(robot_heading))
        heading_row = robot_row + (10 * np.cos(robot_heading))

        # plot the robot heading
        self.__ax.plot([robot_col, heading_col], [robot_row, heading_row], 'r-', linewidth=2)

        # plot the robot pose
        self.__ax.plot(robot_col, robot_row, 'rs', markersize=self.__robot_size)

        # draw new figure
        self.__fig.canvas.draw()

        # Start a time that saves the image ever n seconds
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.saveMapTime:
            self.t = threading.Thread(target=saveMap, args=(self.__fig, self.mapName + f'{self.mapNr:03}',))
            self.t.start()
            self.start_time = time.time()
            self.mapNr += 1

        # wait a bit while the figure is updated (avoids a freeze in Windows)
        import matplotlib.pyplot as plt
        plt.pause(0.01)

    def close(self):
        """ Saves the last image before closing the application """
        saveMap(self.__fig, self.mapName + f'{self.mapNr:03}')
        self.mapNr += 1
        import matplotlib.pyplot as plt
        plt.close()

def saveMap(fig, mapName):
    """ Saves the drawn Map to an Image """
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img = Image.fromarray(data)
    img.convert('RGB').save(mapName + ".png", 'PNG')
