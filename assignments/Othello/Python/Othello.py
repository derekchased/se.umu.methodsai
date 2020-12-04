""" Robot path following implementation based on the Pure Pursuit algorithm """

import sys
import numpy as np
from OthelloPosition import OthelloPosition

class Othello:
  
  # Constructor, takes path filename
  def __init__(self, position, time_limit):
    self._othelloPosition = OthelloPosition(position)


if __name__ == "__main__":
  if(len(sys.argv)>=2):
    othello = Othello(sys.argv[1], sys.argv[2]) 
  else:
    othello = Othello('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE', '7') 
  
