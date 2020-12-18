class OthelloState(object):
    
    def __init__(self, root_player, curr_position, othello_move, curr_ab_depth = 0, max_ab_depth = 1):
        self.root_player = root_player
        self.curr_position = curr_position
        self.othello_move = othello_move
        self.curr_ab_depth = curr_ab_depth
        self.max_ab_depth = max_ab_depth

    def whos_turn(self):
        return "W" if self.curr_position.maxPlayer else "B"

    

    def str_state(self, print_board = False):
    	return "adsasd"#f"{self.curr_position.str_board()}\n {self.root_player} {self.curr_position.maxPlayer} {self.curr_ab_depth} {self.max_ab_depth}" if  print_board else f"{self.root_player} {self.curr_position.maxPlayer} {self.curr_ab_depth} {self.max_ab_depth}"

    def new_state(self, move):
    	new_position = self.curr_position.clone()
    	new_position.make_move(move)
    	new_state = OthelloState(self.root_player, new_position, move, self.curr_ab_depth+1, self.max_ab_depth )
    	return new_state