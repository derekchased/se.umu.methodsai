import numpy as np


class OccupancyGrid:

    def __init__(self, x_anchor, y_anchor, cell_size, row_count, col_count):
        self.x_anchor = x_anchor
        self.y_anchor = y_anchor
        self.cell_size = cell_size
        self.row_count = row_count # height
        self.col_count = col_count # width

        # create grid that is uncertain about every location. 1 = occupied, 0 = empty
        self.__grid = np.ones(shape=(row_count, col_count)) * 0.5

    def get_grid(self):
        return self.__grid

    def set_grid(self, grid):
        self.__grid = grid

    def get_size(self):
        return self.row_count, self.col_count

    def update_grid(self, p_occupied, update_mask):
        """
        Use recursive bayes' rule to update a masked part of the grid at once based on sensor reading.
        """
        prior_occupied = self.__grid
        prior_empty = 1 - self.__grid
        p_empty = 1 - p_occupied

        occupied_term = p_occupied * prior_occupied

        np.putmask(self.__grid, update_mask, occupied_term / (occupied_term + p_empty * prior_empty))

    def wcs_to_grid(self, x_wcs, y_wcs):
        """
        Converts an (x,y) position in the world to a (row,col) coordinate in the grid
        :param x_wcs: x-position in the world
        :param y_wcs: y-position in the world
        :return: A tuple with (row,col)
        """
        col = ((x_wcs - self.x_anchor) / self.cell_size)
        row = ((y_wcs - self.y_anchor) / self.cell_size)
        return row, col

    def grid_to_wcs(self, row_grid, col_grid):
        """
        Converts a (row, col) position in the grid to a (x,y) coordinate in world
        :param row_grid: row index in the grid
        :param col_grid: col index in the grid
        :return: A tuple with (x, y)
        :return: Also works with a numpy arrays of positions
        """
        x_wcs = col_grid * self.cell_size + self.x_anchor
        y_wcs = row_grid * self.cell_size + self.y_anchor
        return x_wcs, y_wcs
