import numpy as np
from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition

class OthelloHeuristics(object):

    def __init__(self, max_player, min_player):
        self.max_player = max_player
        self.min_player = min_player


    def _utility_of_result(self, position ):
        """
        Player has just made a move. This is the resulting position.

        Utility is always Root Player - Opponent Player

        Root = White, Max = True
        Root = White, Max = False

        Root = Black, Max = False
        Root = Black, Max = True

        max, root = white / max = black

        so, I just made a move. Now it is my opponents turn. 
        Did I make a good move?

        
        Args:
            position (TYPE): Description
        
        Returns:
            TYPE: Description
        """

        
        # Number of open spaces indicates how far in the game you are
        # start is 64, and then counts down
        #print("\n_utility_of_result", "B" if position.maxPlayer else "W", ":" + "str(position.move_made)", "," , self.max_player)

        #board = position.board
        #open_spaces = np.sum(position.board == "E") - 36


        board_frameless = position.board[1:9,1:9]

        open_spaces = np.sum(board_frameless == "E")


        # Each players total coins
        max_coins, min_coins = self._utility_coins(board_frameless)
        

        # Each players available moves (regardless of turn)
        max_moves, min_moves = self._utility_moves(position)
        max_moves_len = len(max_moves)
        min_moves_len = len(min_moves)
        

        # Each players corner score (regardless of turn)
        max_num_corners, min_num_corners = self._utility_corners(board_frameless)
        max_stab, min_stab = self._utility_stability(board_frameless)
        max_stab_len = len(max_stab)
        min_stab_len = len(min_stab)
        

        # Calculate overall move value
        heuristic_coin = 100 * (max_coins-min_coins ) / (max_coins + min_coins)
        if( (max_moves_len + min_moves_len) !=0):
            heuristic_mobility = 100 * (max_moves_len-min_moves_len)/(max_moves_len + min_moves_len)
        else:
            heuristic_mobility = 0

        if((max_num_corners+min_num_corners) !=0):
            heuristic_corners = 100* (max_num_corners-min_num_corners)/(max_num_corners+min_num_corners)
        else:
            heuristic_corners = 0

        if((max_stab_len+min_stab_len) !=0):
            heuristic_stability = 100* (max_stab_len-min_stab_len)/(max_stab_len+ min_stab_len)
        else:
            heuristic_stability = 0

        heuristic_total = heuristic_corners*.3 + heuristic_mobility*.2 + heuristic_stability*.25 + heuristic_coin*.25


        """print(self.max_player)
                                print(position.board)
                                print("open_spaces", open_spaces)
                                print("max_coins", max_coins)
                                print("min_coins", min_coins)
                                print("max_moves_len", max_moves_len)
                                print("min_moves_len", min_moves_len)
                                print("max_corners",max_num_corners)
                                print("min_corners",min_num_corners)
                                print("max_stab_len", max_stab_len)
                                print("min_stab_len", min_stab_len)
                                print("heuristic_coin",heuristic_coin)
                                print("heuristic_mobility",heuristic_mobility)
                                print("heuristic_corners",heuristic_corners)
                                print("heuristic_stability",heuristic_stability)
                                print("heuristic_total", heuristic_total)"""

        return OthelloMove(value=heuristic_total)

    def _utility_coins(self, board_frameless):
        return np.sum(board_frameless == self.max_player), np.sum(board_frameless == self.min_player)
    
    def _utility_moves(self, position):
        if( (position.maxPlayer and self.max_player == "W") or 
            (not position.maxPlayer and self.max_player == "B") ):
            max_moves = position.get_moves()
            position.maxPlayer = not position.maxPlayer
            min_moves = position.get_moves()
        elif( (position.maxPlayer and self.max_player == "B") or 
            (not position.maxPlayer and self.max_player == "W")):
            min_moves = position.get_moves()
            position.maxPlayer = not position.maxPlayer
            max_moves = position.get_moves()

        position.maxPlayer = not position.maxPlayer

        return max_moves, min_moves

    def _utility_corners(self, board_frameless):
        corners = np.ma.ones(board_frameless.shape)
        corners[0,0] = corners[0,7] = corners[7,0] = corners[7,7] = False
        masked = np.ma.array(board_frameless,mask=corners)
        max_corners = np.sum(masked == self.max_player)
        min_corners = np.sum(masked == self.min_player)
        return max_corners, min_corners

    def _utility_stability(self, board):
        max_stab = set()
        min_stab = set()
        for transpose in range(2):
            for rotation in range(4):
                token = board[0,0]
                if(token != "E"):
                    stab_set = max_stab if token == self.max_player else min_stab
                    for col in range(len(board)):
                        if(board[0,col] == token):
                            coords = self.rot_coords(transpose, rotation,0,col)
                            stab_set.add(coords)
                        else:
                            break
                board = np.rot90(board)
            board = board.T
        return max_stab, min_stab

    def rot_coords(self, transpose, rotation, row, col):
        if(not transpose):
            if(rotation == 0):
                return (row, col)
            elif(rotation == 1):
                return (col, 7)
            elif(rotation == 2):
                return (7, 7-col)
            else:
                return (7-col, 0)
        else:
            if(rotation == 0):
                return (col, 0)
            elif(rotation == 1):
                return (7, col)
            elif(rotation == 2):
                return (7-col, 7)
            else:
                return (0, 7-col)
        

if __name__ == "__main__":

                                      #1       2       3       4       5       6       7       8
                                      #1234567812345678123456781234567812345678123456781234567812345678
    #root_position = OthelloPosition('WXOXXOOXXXXEEEEOEXXEEEEEEEXEOXEEEOEEXOEEEOOEEEEEEOOOEEEEEXXXXXXXX')
    """root_position = OthelloPosition( 'WEEEEEEEEEEEEEEEEEEEEEEEEEEEOXEEEEEEXOEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                return_move = OthelloMove(row=-1, col=-1, is_pass_move=True)
                if(root_position.maxPlayer):
                    player = "W"
                    opponent = "B"
                else:
                    player = "B"
                    opponent = "W"
                othello_evaluator =  OthelloHeuristics(player, opponent)
                othello_evaluator._utility_of_result(root_position)"""










