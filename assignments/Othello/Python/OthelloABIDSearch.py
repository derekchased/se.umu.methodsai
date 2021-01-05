from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition
import numpy as np
import sys

class OthelloABIDSearch(object):

    """
    The main program of the Othello game search using AB pruning and IDS
    Also performs heuristic evalutation of game positions
    """
    def __init__(self, root_position, return_move, othello_evaluator, min_depth, max_depth, is_alive = True):
        """
        Initialize the alpha beta pruning search with iterative deepening for the
        othello game
        
        Args:
            root_position (OthelloPosition): object representing the board
            return_move (Othello Move): object representing the move that will be
            returned to the shell program
            othello_evaluator (OthelloHeuristics): object representing the heuristics evaluation
            min_depth (int): the initial depth to start iterative deepening from
            max_depth (int): the maximum depth to search using iterative deepening
            is_alive (bool, optional): flag whether the game timer has finished
        """
        self._root_position = root_position
        self._return_move = return_move
        self._othello_evaluator = othello_evaluator
        self._min_depth = min_depth
        self._max_depth = max_depth
        self.is_alive = is_alive

    def ab_id_search( self ):
        """
        Runs the alpha beta search within an iterative deepening for loop. 
        Sets the latest move the player should make on return move object
        """
        if(len(self._root_position.get_moves())):
            self._return_move.is_pass_move = False
            for self._iterative_max_depth in range(self._min_depth, self._max_depth):
                return_move = self._max_search(self._root_position, -np.inf, np.inf, 0)
                if(not self.is_alive):
                    break
                else:
                    self._return_move = return_move
        else:
            self._return_move.is_pass_move = True
    
    def _max_search(self, position, alpha, beta, curr_depth):
        """
        The 'Max' componenet of alpha beta search algorithm. Algorithm
        taken from Russel and Norvig.
        
        Args:
            position (Othello Position): represents the board state
            alpha (float): Description
            beta (float): Description
            curr_depth (int): Description
        
        Returns:
            OthelloMove: Description
        """
        moves = position.get_moves()

        if(self._is_terminal_state(moves, curr_depth)):
            return self._othello_evaluator._utility_of_result(position)

        max_move = OthelloMove(value=-np.inf)

        for i, move in enumerate(moves):
            next_position = self._result(position, move)
            move.value = self._min_search( next_position, alpha, beta, curr_depth+1).value
            max_move = self._max_move(move, max_move)

            if(max_move.value >= beta):
                return max_move
            alpha = alpha if alpha >= max_move.value else max_move.value
        return max_move

    def _min_search(self, position, alpha, beta, curr_depth):
        """
        The 'Min' componenet of alpha beta search algorithm. Algorithm
        taken from Russel and Norvig.
        
        Args:
            position (Othello Position): represents the board state
            alpha (float): Description
            beta (float): Description
            curr_depth (int): Description
        
        Returns:
            OthelloMove: Description
        """
        moves = position.get_moves()
        if(self._is_terminal_state(moves, curr_depth)):
            return self._othello_evaluator._utility_of_result(position)
        
        
        min_move = OthelloMove(value=np.inf)

        for move in moves:
            next_position = self._result(position, move)
            move.value = self._max_search( next_position, alpha, beta, curr_depth+1).value
            min_move = self._min_move(move, min_move)
            
            if(min_move.value <= alpha):
                return min_move
            beta = beta if beta <= min_move.value else min_move.value
        return min_move

    # COMPARATOR
    def _max_move(self, left_move, right_move):
        """
        Compares two OthelloMoves based on their estimated values
        
        Args:
            left_move (OthelloMove): one of two moves
            right_move (OthelloMove): one of two moves
        
        Returns:
            TYPE(OthelloMove): The move with highest value
        """
        return left_move if left_move.value >= right_move.value else right_move

    def _min_move(self, left_move, right_move):
        """
        Compares two OthelloMoves based on their estimated values
        
        Args:
            left_move (OthelloMove): one of two moves
            right_move (OthelloMove): one of two moves
        
        Returns:
            TYPE(OthelloMove): The move with lowest value
        """
        return left_move if left_move.value <= right_move.value else right_move

    def _is_terminal_state(self, moves, curr_depth):
        """
        Determines if state is terminal
        
        Args:
            moves (list): List of available OthelloMove's
            curr_depth (int): The current depth
        
        Returns:
            TYPE(Boolean)
        """
        if(not self.is_alive):
            sys.exit()
        if( moves and curr_depth <= self._iterative_max_depth):
            return False
        return True

    # SIMULATE FUTURE STATES / MAKE MOVE
    def _result(self, position, move):
        """
        Creates a "next move" state, which is a state
        of the board after an action is taken by the current player
        and marks the other player as the current player

        
        Args:
            position (OthelloPosition): the current position
            move (OthelloMove): the move to take
        
        Returns:
            OthelloPosition: The "next" state of the board
        """
        next_position = position.clone()
        next_position.make_move(move)
        return next_position
