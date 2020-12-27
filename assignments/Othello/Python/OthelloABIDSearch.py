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
        self._root_position = root_position
        self._return_move = return_move
        self._othello_evaluator = othello_evaluator
        self._min_depth = min_depth
        self._max_depth = max_depth
        self.is_alive = is_alive
        #self._iterative_max_depth = 1
        #self._branches = 0
        np.random.seed = 42

    def ab_id_search( self ):
        # if no moves available, do nothing, the default move to return is already set to pass
        #print("ab_id_search",len(self._root_position.get_moves()))
        if(len(self._root_position.get_moves())):
            self._return_move.is_pass_move = False
            # perform IDS with AB
            for self._iterative_max_depth in range(self._min_depth, self._max_depth):
                #print("DEPTH",self._iterative_max_depth)
                self._branches = 0
                return_move = self._max_search(self._root_position, -np.inf, np.inf, 0)
                #print("return move, ",return_move)
                #self._root_position.print_board()
                if(not self.is_alive):
                    #print("not alive")
                    break
                else:
                    self._return_move = return_move
                    #print("self._return_move",self._return_move)
        else:
            self._return_move.is_pass_move = True
    
    def _max_search(self, position, alpha, beta, curr_depth):
        moves = position.get_moves()

        if(self._is_terminal_state(moves, curr_depth)):
            return self._othello_evaluator._utility_of_result(position)

        self._branches += 1
        this_branch = self._branches

        max_move = OthelloMove(value=-np.inf)

        for i, move in enumerate(moves):
            next_position = self._result(position, move)
            move.value = self._min_search( next_position, alpha, beta, curr_depth+1).value
            max_move = self._max_move(move, max_move)

            if(max_move.value >= beta):

                
                """print("\n",this_branch)
                                                                print(i, len(moves))
                                                                print(max_move,">= b", beta, "a", alpha)
                                                                for m in moves:
                                                                    print(m)"""

                return max_move
            
            alpha = alpha if alpha >= max_move.value else max_move.value
        
        
        """print("\n",this_branch)
                                print(max_move, "b",beta,"a", alpha)
                                for m in moves:
                                    print(m)"""
        return max_move

    def _min_search(self, position, alpha, beta, curr_depth):
        moves = position.get_moves()
        if(self._is_terminal_state(moves, curr_depth)):
            return self._othello_evaluator._utility_of_result(position)
        
        self._branches += 1
        this_branch = self._branches

        min_move = OthelloMove(value=np.inf)

        for move in moves:
            next_position = self._result(position, move)
            move.value = self._max_search( next_position, alpha, beta, curr_depth+1).value
            min_move = self._min_move(move, min_move)
            
            if(min_move.value <= alpha):
                """print("\n",this_branch)
                                                                print(min_move,"<= a", alpha, "b", beta)
                                                                for m in moves:
                                                                    print(m)"""

                return min_move
            
            beta = beta if beta <= min_move.value else min_move.value

        """print("\n",this_branch)
                                print(min_move, "a",alpha,"b", beta)
                                for m in moves:
                                    print(m)"""
        return min_move

    # COMPARATOR
    def _max_move(self, left_move, right_move):
        return left_move if left_move.value >= right_move.value else right_move

    def _min_move(self, left_move, right_move):
        return left_move if left_move.value <= right_move.value else right_move

    def _is_terminal_state(self, moves, curr_depth):
        if(not self.is_alive):
            sys.exit()
        if( moves and curr_depth <= self._iterative_max_depth):
            return False
        return True

    # SIMULATE FUTURE STATES / MAKE MOVE
    def _result(self, position, move):
        next_position = position.clone()
        #print("\npre result", position.maxPlayer)
        next_position.make_move(move)
        #print("result", next_position.maxPlayer)
        return next_position
