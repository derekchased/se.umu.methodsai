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
		Instantiates and starts a thread timer with the given time limit and a game
		search with the given game string
		
		Args:
		    position_str (str): The serialized game string that represents
		    the starting player and the board
		    time_limit (int): The time limit in seconds
		"""
		# Start timer immediately for fairness
		timer = threading.Timer(time_limit, self._times_up)
		timer.start()
		root_position = OthelloPosition(position_str)
		return_move = OthelloMove(row=-1, col=-1, is_pass_move=True)
		if(root_position.maxPlayer):
			player = "W"
			opponent = "B"
		else:
			player = "B"
			opponent = "W"
		othello_evaluator =  OthelloHeuristics(player, opponent)
		self._othello_ab_id_search = OthelloABIDSearch(root_position, return_move, othello_evaluator, 0, 9, True)
		

	def main(self):
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
			#print("times up")
			#print("self._othello_ab_id_search._return_move",self._othello_ab_id_search._return_move)
			self._othello_ab_id_search._return_move.print_move()
			#print("times up end")
			self._othello_ab_id_search.is_alive = False
			sys.exit()

if __name__ == "__main__":
	
	if(len(sys.argv)>=2):
		othello = Othello(sys.argv[1], int(sys.argv[2])) 
		othello.main()
	else:				#	1		2		3		4		5		6		7		8
		#					1234567812345678123456781234567812345678123456781234567812345678
		othello = Othello('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE', 5) 
		othello.main()

