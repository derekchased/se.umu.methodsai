
import sys
import threading
from OthelloABIDSearch import OthelloABIDSearch
from OthelloPosition import OthelloPosition
from OthelloMove import OthelloMove
from OthelloHeuristics import OthelloHeuristics

class Othello:
	"""
	Container program to receive system arguments and run the game search 
	within the given time limit
	"""

	def __init__(self, position_str, time_limit):
		"""
		Instantiates and starts a thread timer with the given time limit and a game
		search with the given game string
		
		Args:
		    position_str (str): The serialized game string that represents
		    the starting player and the board
		    time_limit (int): The time limit in seconds
		"""
		# Start timer immediately for fairness
		self._timer = threading.Timer(time_limit, self._times_up)
		self._timer.start()
		self._root_position = OthelloPosition(position_str)
		self._return_move = OthelloMove(row=-1, col=-1, is_pass_move=True)
		self._othello_evaluator = OthelloHeuristics("W" if self._root_position.maxPlayer else "B")
		self._othello_ab_id_search = OthelloABIDSearch(self._root_position, self._return_move, self._othello_evaluator, 30, self._timer)
		self._main()

	def _main(self):
		"""
		Run the program within the time limit
		"""
		self._othello_ab_id_search.ab_id_search()
		
	
	def _times_up(self):
		"""Summary
		When the game timer is up, this function will interrupt
		the game search thread and print whatever the most recent
		move is. It will then exit the program (this call might be 
		unnecessary)
		
		Raises:
		    Exception: Generic exception
		"""
		try:
			raise Exception('times up')
		except:
			print("times up")
			print("self._return_move", type(self._return_move),self._return_move)
			self._return_move.print_move()
			self._othello_ab_id_search.is_alive = False

if __name__ == "__main__":
	
	if(len(sys.argv)>=2):
		othello = Othello(sys.argv[1], int(sys.argv[2])) 
	else:
		othello = Othello('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE', 
			5) 


