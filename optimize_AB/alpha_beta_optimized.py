import mancala_v3 as man


class AB_OPTIMIZED:
    def __init__(self, man_obj: man) -> None:
        self.man_obj = man_obj
        
    def switch_player(self, player):
        """
        Switches the current player between 1 and 2.
        """
        return 2 if player == 1 else 1
        
    def utility(self, board: list, player=1):
        """
        Calculates the utility of an outcome for a player based on an integer representing a current state.
        Added a heuristic that leans towards moves that give player more options and not forcing them into having too few pits
        """
        p1_heuristic = 0
        p2_heuristic = 0
        for pit_index in range(self.man_obj.p1_mancala_index): #For every pit on player 1's side
                if board[pit_index]==0: #If player 1 has empty pits...
                    p1_heuristic+=1
                if board[pit_index+self.man_obj.p2_pits_index[0]]==0: #If player 2 has empty pits...
                    p2_heuristic+=1
        if player==1:
            heuristic = (0.5)*(p2_heuristic-p1_heuristic)
            return board[self.man_obj.p1_mancala_index] - board[self.man_obj.p2_mancala_index] + heuristic
        else:
            heuristic = (0.5)*(p1_heuristic-p2_heuristic)
            return board[self.man_obj.p2_mancala_index] - board[self.man_obj.p1_mancala_index] + heuristic


    def max_value(self, board, alpha, beta, depth, player):
        """
        Calculates the maximum value the player can get out of this state.
        """
        
        # terminal = default_state.winning_eval()  # Calculates whether this state is a final state
        terminal = self.man_obj.winning_eval(board, player)
        
        if terminal > 0 or depth == 0:
            return self.utility(board, player), -1  # Calculate the utility of this state for the player whose current turn it is
        value = -1 * (self.man_obj.pits_per_player * self.man_obj.stones_per_pit * 2 + 1)
        pit_to_return = -1
        
        # pits = default_state.valid_moves()  # Figure out what actions are possible (0-index)
        pits = self.man_obj.valid_moves(board, player)
        for pit in pits:  # For every action...
            
            # state = copy.deepcopy(default_state)  # Clone the board state
            new_board = board.copy()
            
            # state.play(pit)  # Play move on this hypothetical board
            self.man_obj.play(pit, new_board, player)
            
            # pit_val, _ = self.min_value(state, alpha, beta, depth - 1, player)  # Determine value after making that move
            pit_val, _ = self.min_value(new_board, alpha, beta, depth - 1, self.switch_player(player))
            
            if pit_val > value:  # If the worst move your opponent can force you into in this state is better than the worst move they can force you into in another state...
                value = pit_val  # Select this value as our best value
                pit_to_return = pit  # Bookmark the pit or action chosen
            if value >= beta: return value, pit_to_return  # Prune if a value is found that is guaranteed to be chosen
            alpha = max(value, alpha)  # Calculate new alpha if needed
        return value, pit_to_return  # Return the value at this state


    def min_value(self, board, alpha, beta, depth, player):
        """
        Calculates the minimum value the player can get out of this state.
        """
        # terminal = default_state.winning_eval()  # Calculates whether this state is a final state
        terminal = self.man_obj.winning_eval(board, player)
        
        if terminal > 0 or depth == 0:
            return self.utility(board, player), -1  # Calculate the utility of this state for the player whose current turn it is
        
        value = self.man_obj.pits_per_player * self.man_obj.stones_per_pit * 2 + 1
        pit_to_return = -1
        
        # pits = default_state.valid_moves()  # Figure out what actions are possible (0-index)
        pits = self.man_obj.valid_moves(board, player)
        
        for pit in pits:  # For every action...
            # state = copy.deepcopy(default_state)  # Clone the board state
            new_board = board.copy()
            
            # state.play(pit)  # Play move on this hypothetical board
            self.man_obj.play(pit, new_board, player)
            
            
            # pit_val, _ = self.max_value(state, alpha, beta, depth - 1, player)  # Determine value after making that move
            pit_val, _ = self.max_value(new_board, alpha, beta, depth - 1, self.switch_player(player))  # Determine value after making that move
            
            
            if pit_val < value:  # If the best move the opponent can make in this state is worse than the best move they can make in another state...
                value = pit_val  # Select this value as our best value
                pit_to_return = pit  # Bookmark the pit or action chosen
            if value <= alpha: return value, pit_to_return  # Prune if a value is found that is guaranteed to be chosen
            beta = min(value, beta)  # Calculate new beta if needed
        return value, pit_to_return  # Return the value at this state


    def alphabeta_search(self, depth, player=1):
        """
        Performs AlphaBeta on the Mancala game.
        """
        
        beta = self.man_obj.pits_per_player * self.man_obj.stones_per_pit * 2 + 1
        alpha = -beta
        board = self.man_obj.board.copy()
        # state = copy.deepcopy(self)
        value, pit = self.max_value(board, alpha, beta, depth, player)
        return pit