import numpy as np


class OccupancyGrid:

    def __init__(self, x_anchor, y_anchor, cell_size, row_count, col_count):
        self.x_anchor = x_anchor
        self.y_anchor = y_anchor
        self.cell_size = cell_size
        self.row_count = row_count
        self.col_count = col_count

        # create grid that is uncertain about every location. 1 = occupied, 0 = empty
        self.__grid = np.ones(shape=(row_count, col_count)) * 0.5

    def get_grid(self):
        return self.__grid

    def get_size(self):
        return {'rows': self.row_count, 'cols': self.col_count}

    def update_cell(self, x_grid, y_grid, p_occupied):
        """
        Use recursive bayes' rule to update grid value based on sensor reading.
        """
        if x_grid >= self.row_count or y_grid >= self.col_count:
            return
        if x_grid < 0 or y_grid < 0:
            return

        prior_occupied = self.__grid[x_grid][y_grid]
        prior_empty = 1 - prior_occupied

        self.__grid[x_grid][y_grid] = (p_occupied * prior_occupied)/(p_occupied * prior_occupied + (1 - p_occupied) * prior_empty)

    def pos_to_grid(self, x_wcs, y_wcs):
        """
        Converts an (x,y) position in the world to a (row,col) coordinate in the grid
        :param x_wcs: x-position in the world
        :param y_wcs: y-position in the world
        :return: A tuple with (row,col)
        """
        col = ((x_wcs - self.x_anchor) / self.cell_size)
        row = ((y_wcs - self.y_anchor) / self.cell_size)
        return row, col
