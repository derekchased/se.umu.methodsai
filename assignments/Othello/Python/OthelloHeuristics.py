import numpy as np


class OthelloHeuristics(object):

    def __init__(self, root_player):
        self.root_player = root_player

    def _utility_of_result(self, position ):
        return np.random.uniform()
        #if(not self._thread_timer.is_alive()):
         #   raise Exception('times up')
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
        #if(not self._thread_timer.is_alive()):
         #   raise Exception('times up')

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