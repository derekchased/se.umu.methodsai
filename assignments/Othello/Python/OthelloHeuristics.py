import numpy as np
from OthelloMove import OthelloMove
from OthelloPosition import OthelloPosition

class OthelloHeuristics(object):

    def __init__(self, max_player, min_player):
        """
        Instantiates a heuristics object and stores which color
        player is max and which is min
        
        Args:
            max_player (str): The max player of the game (not the move) "W" or "B"
            min_player (str): The min player of the game (not the move) "W" or "B"
        """
        self.max_player = max_player
        self.min_player = min_player


    def _utility_of_result(self, position ):
        """
        Calculates the value of the board, regardless of who's turn
        
        Args:
            position (OthelloPosition): The position to evaluate
        
        Returns:
            OthelloMove: an OthelloMove object with the value estimated
        """
        board_frameless = position.board[1:9,1:9]
        #open_spaces = np.sum(board_frameless == "E")

        # Coins
        max_coins, min_coins = self._utility_coins(board_frameless)
        heuristic_coin = 100 * (max_coins-min_coins ) / (max_coins + min_coins)

        # Mobility
        max_moves, min_moves = self._utility_moves(position)
        max_moves_len = len(max_moves)
        min_moves_len = len(min_moves)
        if( (max_moves_len + min_moves_len) !=0):
            heuristic_mobility = 100 * (max_moves_len-min_moves_len)/(max_moves_len + min_moves_len)
        else:
            heuristic_mobility = 0

        # Corners
        max_num_corners, min_num_corners = self._utility_corners(board_frameless)
        if((max_num_corners+min_num_corners) !=0):
            heuristic_corners = 100* (max_num_corners-min_num_corners)/(max_num_corners+min_num_corners)
        else:
            heuristic_corners = 0

        # Stability
        max_stab, min_stab = self._utility_stability(board_frameless)
        max_stab_len = len(max_stab)
        min_stab_len = len(min_stab)
        if((max_stab_len+min_stab_len) !=0):
            heuristic_stability = 100* (max_stab_len-min_stab_len)/(max_stab_len+ min_stab_len)
        else:
            heuristic_stability = 0

        heuristic_total = heuristic_corners*.3 + heuristic_mobility*.2 + heuristic_stability*.25 + heuristic_coin*.25

        return OthelloMove(value=heuristic_total)

    def _utility_coins(self, board_frameless):
        """
        Calculates the total number of coins each player has
        
        Args:
            board_frameless (numpy): An array representation of the board
        
        Returns:
            tuple(int,int): max player's coins, min player's coins
        """
        return np.sum(board_frameless == self.max_player), np.sum(board_frameless == self.min_player)
    
    def _utility_moves(self, position):
        """
        Calculates the number of moves available to max and min players
        
        Args:
            position (OthelloPosition): The position to evaluate
        
        Returns:
            tuple(int, int): num max's moves, num min's moves
        """
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
        """
        Number of corner positions held by each player
        
        Args:
            board_frameless (numpy): An array representation of the board
        
        Returns:
            tuple(int, int): num max's corners, num min's corners
        """
        corners = np.ma.ones(board_frameless.shape)
        corners[0,0] = corners[0,7] = corners[7,0] = corners[7,7] = False
        masked = np.ma.array(board_frameless,mask=corners)
        max_corners = np.sum(masked == self.max_player)
        min_corners = np.sum(masked == self.min_player)
        return max_corners, min_corners

    def _utility_stability(self, board_frameless):
        """
        Calculate the "stability" value of each player. In this case,
        the stability is simply the number of coins along the edge, including
        corners, that cannot be flipped by the other player

        This implementation uses numpy matrix rotations to evaluate the edges.
        It essentially only calculates from top left to top right, and then
        uses the helper function rot_coords to further help with translating
        the matrix rotations (I found this preferable to keeping track of index pointers)
        
        Args:
            board_frameless (numpy): An array representation of the board
        
        Returns:
            tuple(int, int): max's "stability" value, min's "stability" value
        """
        max_stab = set()
        min_stab = set()
        for transpose in range(2):
            for rotation in range(4):
                token = board_frameless[0,0]
                if(token != "E"):
                    stab_set = max_stab if token == self.max_player else min_stab
                    for col in range(len(board_frameless)):
                        if(board_frameless[0,col] == token):
                            coords = self.rot_coords(transpose, rotation,0,col)
                            stab_set.add(coords)
                        else:
                            break
                board_frameless = np.rot90(board_frameless)
            board_frameless = board_frameless.T
        return max_stab, min_stab

    def rot_coords(self, transpose, rotation, row, col):
        """
        Helper function to _utility_stability which translates
        indexes/element-positions from the rotated matrix to the original
        matrix
        
        Args:
            transpose (int): 0 or 1
            rotation (int): 0, 1, 2, or 3
            row (int): the row index of the rotated matrix
            col (int): the col index of the rotated matrix
        
        Returns:
            tuple(int): the corresponding (row,col) of the original matrix
        """
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
