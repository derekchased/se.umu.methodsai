from OthelloState import OthelloState
from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition
import numpy as np

class OthelloABSearch(object):

    def __init__(self, position_str):
        # Initialize
        self._root_position = OthelloPosition(position_str)
        self._root_player = "W" if self._root_position.maxPlayer else "B"
        self._othello_move = OthelloMove(0, 0, True)
        self.othello_state = OthelloState(self._root_player, self._root_position, 0, 1)
    

    # AB SEARCH
    def absearch( self, othello_state ):
        print("absearch\n", othello_state.str_state(True))
        max_move = self._max_value(othello_state, OthelloMove(value=-np.inf, name="alpha"), OthelloMove(value=np.inf, name="beta"))
        print("absearch complete", max_move.str_move())

    def _max_value(self, othello_state, alpha, beta):
        print("_max_value", othello_state.str_state(), alpha.str_move(), beta.str_move())
        
        tt = self._terminalTest(othello_state)
        if(tt):
            return self.utility(othello_state)
        moves = othello_state.curr_position.get_moves()
        max_move = OthelloMove(value=-np.inf)

        print(len(moves))
        for i, move in enumerate(moves):
            print(i)
            move.print_move()
            result = self._result(othello_state, move)
            print("result", result.str_state())
            max_move = self._max_move(max_move, self._min_value( result, alpha, beta))
            if(max_move.value >= beta.value):
                return max_move
            alpha = self._max_move(alpha, max_move)

        return max_move

    def _max_move(self, left_move, right_move):
        print("_max_move")
        print("left_move: ", left_move.str_move())
        print("right_move: ", right_move.str_move())

        return left_move if left_move.value >= right_move.value else right_move

    def _min_value(self, othello_state, alpha, beta):
        print("_min_value", othello_state.str_state(), alpha.str_move(), beta.str_move())
        
        tt = self._terminalTest(othello_state)
        if(tt):
            return self.utility(othello_state)
        
        min_move = OthelloMove(value=np.inf)

        moves = othello_state.curr_position.get_moves()

        print(len(moves))
        
        for i, move in enumerate(moves):
            print(i)
            move.print_move()
            result = self._result(othello_state, move)
            print("result", result.str_state())
            
            min_move = self._min_move(min_move, self._max_value( result, alpha, beta))
            
            if(min_move.value <= alpha.value):
                return min_move
            beta = self._min_move(beta, min_move)

        return min_move

    def _min_move(self, left_move, right_move):
        print("_min_move")
        print("left_move: ", left_move.str_move())
        print("right_move: ", right_move.str_move())

        return left_move if left_move.value < right_move.value else right_move

    def _result(self, othello_state, move):
        print("_result")
        new_state = othello_state.new_state(move)
        print("new_state",new_state.str_state(print_board = True))
        return new_state

    def _utility(self ):
        """Calculates value of current state
        
        Args:
            maxPlayer (str): Indicate MAX player, ie, who's turn this is
            position (OthelloPosition): Current state of the board
        
        Returns:
            float: a value from -1 to 1
        """
        return np.random.uniform(-1,1 )

    def _terminalTest(self, othello_state):
        """Perform a terminal test 
            - game could be over
        
        Args:
            maxPlayer (str): Indicates which player is MAX, ie, who's turn is this
            position (OthelloPosition): Representation of the board
        
        Returns:
            bool: True of state is terminal
        """
        if(len(othello_state.curr_position.get_moves())):
            return False
        return True

if __name__ == "__main__":        
    othello_ab_search = OthelloABSearch('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    othello_ab_search.absearch(othello_ab_search.othello_state)