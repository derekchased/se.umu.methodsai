""" Robot path following implementation based on the Pure Pursuit algorithm """

import sys
import threading
from OthelloABSearch import OthelloABSearch

class Othello:

	# Constructor, takes path filename
	def __init__(self, position_str, time_limit):
		
		# Start the move timer
		#self._timer = threading.Timer(time_limit, self._times_up) 
		#self._timer.start() 

		self._othello_ab_search = OthelloABSearch(position_str)
		self._othello_ab_search.absearch( self._othello_ab_search.othello_state)

	# Game Timer
	def _times_up(self): 
		pass

	# HEURISTICS
	def _coin_parity(self):
		"""Summary
		
		Args:
		    is_white_turn (bool): Description
		    board (OthelloPosition): Description
		
		Returns:
		    int: Description
		"""
		diff_coins = 10

		return diff_coins

	def _player_coins(self, is_white, othello_position):
		return np.sum(othello_position.board == ("W" if is_white else "B"))


if __name__ == "__main__":
	if(len(sys.argv)>=2):
		othello = Othello(sys.argv[1], int(sys.argv[2])) 
	else:
		othello = Othello('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE', 
			3) 


