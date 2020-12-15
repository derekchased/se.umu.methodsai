from OthelloState import OthelloState
from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition
import numpy as np

class OthelloABSearch(object):

    def __init__(self, position_str):
        # Initialize
        self._root_position = OthelloPosition(position_str)
        self._max_player = "W" if self._root_position.maxPlayer else "B"
        self._min_player = "B" if self._root_position.maxPlayer else "W"
        self._othello_move = OthelloMove()
        self.othello_state = OthelloState(self._max_player, self._root_position, self._othello_move, 0,4)
        np.random.seed(42)

    # AB SEARCH
    def absearch( self, othello_state ):
        #print("absearch\n", othello_state.str_state(True))
        max_move = self._max_value(othello_state, -np.inf, np.inf)
        #print("absearch complete", max_move.str_move())

    def _max_value(self, othello_state, alpha, beta):
        
        if(self._terminal_test(othello_state)):
            
            return self._utility(othello_state)

        moves = othello_state.curr_position.get_moves()
        
        max_move = OthelloMove(value=-np.inf)

        for move in moves:

            result = self._result_state(othello_state, move)
            move.value = self._min_value( result, alpha, beta).value
            max_move = self._max_move(max_move, move)

            if(max_move.value >= beta):
                #print("beta max",max_move.str_move())
                return max_move
            
            alpha = alpha if alpha >= max_move.value else max_move.value
        
        #print("max",max_move.str_move())
        return max_move

    def _min_value(self, othello_state, alpha, beta):
        
        if(self._terminal_test(othello_state)):
            return self._utility(othello_state)
        
        moves = othello_state.curr_position.get_moves()

        min_move = OthelloMove(value=np.inf)

        for move in moves:
            
            result = self._result_state(othello_state, move)
            move.value = self._max_value( result, alpha, beta).value
            min_move = self._min_move(min_move, move)
            if(min_move.value <= alpha):
                #print("alpha min",min_move.str_move())
                return min_move
            
            beta = beta if beta <= min_move.value else min_move.value
        
        #print("min",min_move.str_move())
        return min_move

    # COMPARATOR
    def _max_move(self, left_move, right_move):
        return left_move if left_move.value >= right_move.value else right_move

    def _min_move(self, left_move, right_move):
        return left_move if left_move.value <= right_move.value else right_move

    def _terminal_test(self, othello_state):
        if( len(othello_state.curr_position.get_moves()) and 
            othello_state.curr_ab_depth < othello_state.max_ab_depth):
            return False
        return True

    # SIMULATE FUTURE STATES / MAKE MOVE
    def _result_state(self, othello_state, move):
        new_state = othello_state.new_state(move)
        return new_state

    # UTILITIES
    def _utility(self, othello_state ):
        
        coins = _utility_coins(othello_state)

        opponent_moves = othello_state.curr_position.get_moves()

        corners = _utility_corners(othello_state, opponent_moves)

        utility_moves = _utility_moves(othello_state, opponent_moves)
        
        

        othello_state.othello_move.value = np.random.uniform(0, 1)
        #print(othello_state.othello_move.str_move())
        return othello_state.othello_move

    def _utility_corners(self, othello_state, opponent_moves):
        # can opponent take a corner now?

        # can I take a corner next?
        pass

    def _utility_coins(self, othello_state):
        # count coins
        coin_difference = np.sum(othello_state.curr_position.board == self._max_player) - np.sum(othello_state.curr_position.board == self._min_player)
        return coin_difference

    def _utility_moves(self, othello_state, opponent_moves):
        #print("\ncoin_difference",coin_difference)
        num_opponent_moves = len(opponent_moves)
        #print("opponent_moves",len(opponent_moves))
        total_next_moves = 0 
        for move in opponent_moves:
            next_state = self._result_state(othello_state,move)
            total_next_moves = total_next_moves + len(next_state.curr_position.get_moves())
        #print("total_next_moves",total_next_moves)
        avg_next_moves = total_next_moves/len(opponent_moves)
        #print("avg_next_moves",avg_next_moves)


    

if __name__ == "__main__":        
    othello_ab_search = OthelloABSearch('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    othello_ab_search.absearch(othello_ab_search.othello_state)