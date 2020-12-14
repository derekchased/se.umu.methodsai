from OthelloState import OthelloState
from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition
import numpy as np

class OthelloABSearch(object):

    def __init__(self, position_str):
        # Initialize
        self._root_position = OthelloPosition(position_str)
        self._root_player = "W" if self._root_position.maxPlayer else "B"
        self._othello_move = OthelloMove()
        self.othello_state = OthelloState(self._root_player, self._root_position, self._othello_move, 0, 2)
    

    # AB SEARCH
    def absearch( self, othello_state ):
        print("absearch\n", othello_state.str_state(True))
        moves = othello_state.curr_position.get_moves()
        for move in moves:
            print move.str_move()
        max_move = self._max_value(othello_state, OthelloMove(value=-np.inf, name="alpha"), OthelloMove(value=np.inf, name="beta"))
        print("absearch complete", max_move.str_move())

    def _max_value(self, othello_state, alpha, beta):
        
        tt = self._terminalTest(othello_state)
        if(tt):
            return self._utility(othello_state)
        moves = othello_state.curr_position.get_moves()
        max_move = OthelloMove(value=-np.inf)
        print("_max_value, moves:", len(moves) )
        for i, move in enumerate(moves):
            print("_max_value",i,move.str_move())
            result = self._result(othello_state, move)
            max_move = self._max_move(max_move, self._min_value( result, alpha, beta))
            if(max_move.value >= beta.value):
                print("return max_move.value >= beta.value", max_move.value,">=", beta.value)
                return max_move
            print("update alpha",alpha.str_move())
            alpha = self._max_move(alpha, max_move)
            print("after",alpha.str_move())

        print("return max_move", max_move.str_move())
        return max_move

    def _max_move(self, left_move, right_move):
        return left_move if left_move.value >= right_move.value else right_move

    def _min_value(self, othello_state, alpha, beta):
        tt = self._terminalTest(othello_state)
        if(tt):
            return self._utility(othello_state)
        
        min_move = OthelloMove(value=np.inf)

        moves = othello_state.curr_position.get_moves()

        print("_min_value, moves:", len(moves) )
        for i, move in enumerate(moves):
            print("_min_value",i,move.str_move())
            result = self._result(othello_state, move)
            min_move = self._min_move(min_move, self._max_value( result, alpha, beta))
            if(min_move.value <= alpha.value):
                print("return min_move.value <= alpha.value",min_move.value,"<=",alpha.value)
                return min_move
            print("update beta",beta.str_move())
            beta = self._min_move(beta, min_move)
            print("after",beta.str_move())

        print("return min_move", min_move.str_move())
        return min_move

    def _min_move(self, left_move, right_move):
        return left_move if left_move.value < right_move.value else right_move

    def _result(self, othello_state, move):
        new_state = othello_state.new_state(move)
        return new_state

    def _utility(self, othello_state ):
        othello_state.othello_move.value = np.random.uniform(-1, 1)
        return othello_state.othello_move

    def _terminalTest(self, othello_state):
        if( len(othello_state.curr_position.get_moves()) and 
            othello_state.curr_ab_depth < othello_state.max_ab_depth):
            return False
        return True

if __name__ == "__main__":        
    othello_ab_search = OthelloABSearch('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    othello_ab_search.absearch(othello_ab_search.othello_state)