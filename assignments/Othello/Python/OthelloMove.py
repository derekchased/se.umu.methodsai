class OthelloMove(object):
    """
      This class represents a 'move' in a game.
      The move is simply represented by two integers: the row and the column where the player puts the marker and a
      boolean to mark if it is a pass move or not.
      In addition, the OthelloMove has a field where the estimated value of the move can be stored during
      computations.

      Author: Ola Ringdahl
    """

    def __init__(self, row=-1, col=-1, is_pass_move=False, value="", path=None):
        """
        Creates a new OthelloMove for (row, col) with value 0.
        :param row: Row
        :param col: Column
        :param is_pass_move: True if it is a pass move
        """
        self.row = row
        self.col = col
        self.is_pass_move = is_pass_move
        self.value = value
        self.path = path

    def print_move(self):
        """
        Prints the move on the format (3,6) or Pass
        :return: Nothing
        """
        if self.is_pass_move:
            print("pass")
        else:
            print("(" + str(self.row) + "," + str(self.col)+ ")")

    def __repr__(self):
      if self.is_pass_move:
        return "pass"
      else:
        return "("+str(self.value)+"," + str(self.row) + "," + str(self.col) + ")"
