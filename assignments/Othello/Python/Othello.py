""" Robot path following implementation based on the Pure Pursuit algorithm """

import sys
import threading
from OthelloABSearch import OthelloABSearch

class Othello:

	# Constructor, takes path filename
	def __init__(self, position_str, time_limit):
		#print(" Othello __init__ ")
		# Start the move timer
		#print(" self._times_up " , time_limit)

		self._timer = threading.Timer(time_limit, self._times_up) 
		self._timer.start() 
		

		self._othello_ab_search = OthelloABSearch(position_str, self._timer)
		self._othello_ab_search.run()

	# Game Timer
	def _times_up(self):
		#thread.interrupt_main()
		#print(" self._times_up () " , self._times_up)
		self._othello_ab_search._othello_move.print_move()
		#print(" self._times_up () " , self._times_up)
		exit() 

if __name__ == "__main__":
	#othello = Othello(sys.argv[1], int(sys.argv[2])) 
	if(len(sys.argv)>=2):
		othello = Othello(sys.argv[1], int(sys.argv[2])) 
	else:
		othello = Othello('BEEEEOEEEEEEEOEEEEEEEOEEEEEEOOEEEEEEXOOOEEEXEEEEEEXEEEEEEEEEEEEEE', 
			10) 


