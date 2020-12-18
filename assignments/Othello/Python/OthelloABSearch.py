from OthelloState import OthelloState
from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition
import numpy as np

class OthelloABSearch(object):

    def __init__(self, position_str, thread_timer):
        
        # Initialize
        #print("init ab search")
        
        np.random.seed(42)

        self._thread_timer = thread_timer
        self._root_position = OthelloPosition(position_str)
        self._max_player = "W" if self._root_position.maxPlayer else "B"
        self._min_player = "B" if self._root_position.maxPlayer else "W"
        self._othello_move = OthelloMove(is_pass_move=True)
        #self.othello_state = OthelloState(self._max_player, self._root_position, self._othello_move, 0, 5)

        
        
    def run(self):
        moves = []
        for max_depth in range (1,3):
            #print("max_depth",max_depth)
            #print(moves)
            moves.sort(key=lambda x:x.value, reverse=True)
            #print(moves)
            for move in moves:
                move.value = ""
            
            moves = self.absearch(OthelloState(self._max_player, self._root_position, OthelloMove(), 0, max_depth),moves)
            
        #self._othello_move.print_move()


    # AB SEARCH
    def absearch( self, othello_state, moves=[]):
        #print("absearch\n", othello_state.str_state(True))
        try:
            max_move, moves = self._max_value(othello_state, -np.inf, np.inf, True, True if len(moves) else False, moves)
        except:
            #print("error")
            max_move = self._othello_move
            moves = []
            

        self._othello_move = max_move
        #print("absearch complete", max_move, moves)
        return moves

    def _max_value(self, othello_state, alpha, beta, return_moves = False, use_pass_in_moves = False, pass_in_moves=[]):
        if(not self._thread_timer.is_alive()):
            raise Exception('times up')


        #print("a")
        if(self._terminal_test(othello_state)):
         #   print("b")
            abc = self._utility(othello_state)
            #print(abc, type(abc))
            return self._utility(othello_state)

        if(use_pass_in_moves):
            moves = pass_in_moves
        else:
            moves = othello_state.curr_position.get_moves()
        
        max_move = OthelloMove(value=-np.inf)

        for move in moves:
            if(not self._thread_timer.is_alive()):
                raise Exception('times up')

            result = self._result_state(othello_state, move)
            move.value = self._min_value( result, alpha, beta).value
            max_move = self._max_move(max_move, move)

            if(max_move.value >= beta):
                #print(moves)
                if(return_moves):
                    return max_move, moves
                return max_move
            
            alpha = alpha if alpha >= max_move.value else max_move.value
        
        #print(moves)
        if(return_moves):
            return max_move, moves
        return max_move

    def _min_value(self, othello_state, alpha, beta):
        if(not self._thread_timer.is_alive()):
            raise Exception('times up')

        if(self._terminal_test(othello_state)):
            return self._utility(othello_state)
        
        moves = othello_state.curr_position.get_moves()

        min_move = OthelloMove(value=np.inf)

        for move in moves:
            if(not self._thread_timer.is_alive()):
                raise Exception('times up')
            
            result = self._result_state(othello_state, move)
            move.value = self._max_value( result, alpha, beta).value
            min_move = self._min_move(min_move, move)
            if(min_move.value <= alpha):
                #print(moves)
                return min_move
            
            beta = beta if beta <= min_move.value else min_move.value
        
        #print(moves)
        return min_move

    # COMPARATOR
    def _max_move(self, left_move, right_move):
        return left_move if left_move.value >= right_move.value else right_move

    def _min_move(self, left_move, right_move):
        return left_move if left_move.value <= right_move.value else right_move

    def _terminal_test(self, othello_state):
        if(not self._thread_timer.is_alive()):
            raise Exception('times up')
        #print("C")
        #print( len(othello_state.curr_position.get_moves()  ))
        
        if( len(othello_state.curr_position.get_moves()) and othello_state.curr_ab_depth < othello_state.max_ab_depth):
         #   print("D")
            return False
        #print("E")
        return True

    # SIMULATE FUTURE STATES / MAKE MOVE
    def _result_state(self, othello_state, move):
        new_state = othello_state.new_state(move)
        return new_state

    # UTILITIES
    def _utility(self, othello_state ):
        if(not self._thread_timer.is_alive()):
            raise Exception('times up')
        """print("\nutility")
                                print( "state max", self._max_player)
                                print( "self root", othello_state.root_player)
                                print( "pos max",   othello_state.curr_position.maxPlayer)
                                print( "state whos turn",   othello_state.whos_turn())
                        
                                
                                print(othello_state.curr_position.maxPlayer)"""

        coin_difference = self._utility_coins(othello_state)
        #print("coin_difference", coin_difference)

        opponent_moves = othello_state.curr_position.get_moves()
        len_opponent_moves = len(opponent_moves)
        
        #print("opponent_moves", len_opponent_moves)

        utility_moves = self._utility_moves(othello_state, opponent_moves)
        #print("utility_moves", utility_moves)

        my_corners, opponent_corners = self._utility_corners(othello_state, opponent_moves)

        opponent_corners *= -4
        my_corners *=3

        othello_state.othello_move.value = coin_difference*.1 + (utility_moves-len_opponent_moves)*.4 + my_corners*.25 + opponent_corners*.25

        if(not len_opponent_moves):
            othello_state.othello_move.value += 5
            othello_state.othello_move.is_pass_move = True

        #print(othello_state.othello_move)
        """
                                print("\nutility",othello_state.whos_turn(), othello_state.othello_move.value)
                                othello_state.curr_position.print_board()
                                print("coin_difference",coin_difference)
                                print("utility_moves",utility_moves)
                                print("len_opponent_moves",len_opponent_moves)
                                print("my_corners",my_corners)
                                print("opponent_corners",opponent_corners)"""
        

        return othello_state.othello_move

    def _utility_corners(self, othello_state, opponent_moves):
        # can opponent take a corner now?
        opponent_corners = 0
        my_corners = 0
        corners = [(1,1), (1,8), (8,8), (8,1)]
        avail_corners = []

        for corner in corners:
            if(othello_state.curr_position.board[corner[0],corner[1]] == "E"):
                avail_corners.append(corner)


        #print("avail_corners ", avail_corners)


        for opponent_move in opponent_moves:
            for avail_corner in avail_corners:
                if(opponent_move.row == corner[0] and opponent_move.col == corner[1]):
                    opponent_corners += 1

            next_state = self._result_state(othello_state,opponent_move)
            next_moves = next_state.curr_position.get_moves()
            
            for next_move in next_moves:
                for corner in avail_corners:
                    if(next_move.row == corner[0] and opponent_move.col == corner[1]):
                        my_corners += 1




        #print("_utility_corners", opponent_corners)
        # can I take a corner next?
        #return 0,0
        return my_corners, opponent_corners

    def _utility_coins(self, othello_state):
        # count coins
        coin_difference = np.sum(othello_state.curr_position.board == self._max_player) - np.sum(othello_state.curr_position.board == self._min_player)
        return coin_difference

    def _utility_moves(self, othello_state, opponent_moves):
        if(not self._thread_timer.is_alive()):
            raise Exception('times up')

        #print("\ncoin_difference",coin_difference)
        num_opponent_moves = len(opponent_moves)

        if(num_opponent_moves):
            #print("opponent_moves",len(opponent_moves))
            total_next_moves = 0 
            for move in opponent_moves:
                next_state = self._result_state(othello_state,move)
                total_next_moves = total_next_moves + len(next_state.curr_position.get_moves())
            #print("total_next_moves",total_next_moves)
            avg_next_moves = total_next_moves/len(opponent_moves)
            return avg_next_moves
        else:
            next_state = othello_state.new_state(OthelloMove(is_pass_move=True))
            total_next_moves = len(next_state.curr_position.get_moves())
            return total_next_moves

        


    

if __name__ == "__main__":        
    othello_ab_search = OthelloABSearch('WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    #othello_ab_search = OthelloABSearch('')
    #othello_ab_search = OthelloABSearch('BOOOOOOOOOOOOOOOOOOOOOOXOOOXOXXXOOXOOOXOOXOOOOOOOOOOOOOOOOOOOOOOE')
    
    othello_ab_search.run()
    #othello_ab_search.absearch(othello_ab_search.othello_state)