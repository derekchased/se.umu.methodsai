import sys
import threading
from OthelloABIDSearch import OthelloABIDSearch
from OthelloPosition import OthelloPosition
from OthelloMove import OthelloMove
from OthelloHeuristics import OthelloHeuristics

class Othello():
	"""
	Container program to receive system arguments and run the game search 
	within the given time limit
	"""

	def __init__(self, position_str, time_limit):
		"""
		Instantiates components needed for the game including timer, root position and
		root player, return move, heuristics and search
		
		Args:
		    position_str (str): The serialized game string that represents
		    the starting player and the board
		    time_limit (int): The time limit in seconds
		"""
		self._timer = threading.Timer(time_limit, self._times_up)
		
		root_position = OthelloPosition(position_str)
		return_move = OthelloMove(row=-1, col=-1, is_pass_move=True)
		
		if(root_position.maxPlayer):
			player = "W"
			opponent = "B"
		else:
			player = "B"
			opponent = "W"
		othello_evaluator =  OthelloHeuristics(player, opponent)
		
		self._othello_ab_id_search = OthelloABIDSearch(root_position, return_move, othello_evaluator, 2, 30, True)
		

	def main(self):
		"""
		Start the game
		"""
		self._timer.start()
		self._othello_ab_id_search.ab_id_search()
		
	
	def _times_up(self):
		"""Summary
		When the game timer is up, this function will interrupt
		the game search thread (Iterative deepening search) and print 
		whatever the most recent move is and exit the program
		
		Raises:
		    Exception: Generic exception
		"""
		try:
			raise Exception('times up')
		except:
			self._othello_ab_id_search._return_move.print_move()
			self._othello_ab_id_search.is_alive = False
			sys.exit()

if __name__ == "__main__":
	if(len(sys.argv)>=3):
		game_str = sys.argv[1]
		if(len(game_str) != 65):
			print('Incorrect game string length')	
			sys.exit()
		time_limit = int(sys.argv[2])
		othello = Othello(game_str, time_limit) 
		othello.main()
	else:
		print('Incorrect number of arguments')
		sys.exit()