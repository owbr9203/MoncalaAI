import random
from random import choice
random.seed(109)  # Seeds the random number generator for reproducibility

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        Initializes the Mancala game with specified number of pits and stones per pit.
        """
        self.pits_per_player = pits_per_player  # Sets the number of pits per player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2  # Number of players in the game
        self.current_player = 1  # Initializes the current player to 1
        self.moves = []  # List to keep track of moves made
        self.p1_pits_index = [0, self.pits_per_player-1]  # Indexes for player 1's pits
        self.p1_mancala_index = self.pits_per_player  # Index for player 1's mancala
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]  # Indexes for player 2's pits
        self.p2_mancala_index = len(self.board)-1  # Index for player 2's mancala
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0  # Sets player 1's mancala to 0
        self.board[self.p2_mancala_index] = 0  # Sets player 2's mancala to 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]  # Extracts player 1's pits
        player_1_mancala = self.board[self.p1_mancala_index]  # Extracts player 1's mancala
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]  # Extracts player 2's pits
        player_2_mancala = self.board[self.p2_mancala_index]  # Extracts player 2's mancala

        print('P1               P2')  # Header for the board display
        print('     ____{}____     '.format(player_2_mancala))  # Displays player 2's mancala
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))  # Displays the last pit of player 1 and the first pit of player 2
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))  # Displays the pits of both players
            
        print('         {}         '.format(player_1_mancala))  # Displays player 1's mancala
        turn = 'P1' if self.current_player == 1 else 'P2'  # Determines whose turn it is
        print('Turn: ' + turn)  # Displays whose turn it is
        
    def valid_move(self, pit):
        """
        Checks if the pit chosen by the current_player is a valid move.
        """
        
        if pit < 0 or pit >= len(self.board): return False  # Checks if the pit is within the board bounds
        if pit in [self.p1_mancala_index, self.p2_mancala_index] or self.board[pit] <= 0: return False  # Checks if the pit is a mancala or is empty
        
        return True  # If all checks pass, the move is valid
        
    def random_move_generator(self):
        """
        Generates random valid moves with non-empty pits for the random player
        """
        
        if self.current_player==1:
            options = [pit for pit in range(1,self.pits_per_player+1) if self.valid_move(pit)]
        else:
            options = [pit for pit in range(1,self.pits_per_player+1) if self.valid_move(pit)]
        return choice(options)
    
    def play(self, pit):
        """
        Simulates a single move made by a specific player using their selected pit.
        """
        pit -= 1 # 1 based index  # Adjusts the pit index to 0-based
        if not self.valid_move(pit):
            print("INVALID MOVE")
            return  # Exits if the move is invalid
        
        if self.winning_eval() != 0:
            print("GAME OVER")
            return  # Exits if the game is over
        
        stones = self.board[pit]  # Number of stones in the selected pit
        self.board[pit] = 0  # Empties the selected pit
        current_pit = pit  # Sets the current pit to the selected pit
        
        while stones > 0:
            current_pit = (current_pit + 1) % len(self.board)  # Moves to the next pit
            if (self.current_player == 1 and current_pit == self.p2_mancala_index) or (
                    self.current_player == 2 and current_pit == self.p1_mancala_index):
                current_pit = (current_pit + 1) % len(self.board)  # Skips the opponent's mancala
            self.board[current_pit] += 1  # Drops a stone in the current pit
            stones -= 1  # Decrements the number of stones

        # checks for if you end on pit
        if self.current_player == 1 and current_pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1) and self.board[current_pit] == 1:
            opposite_pit = self.p2_mancala_index - current_pit - 1  # Calculates the opposite pit
            if self.board[opposite_pit] > 0:
                self.board[self.p1_mancala_index] += self.board[opposite_pit] + 1  # Captures the stones in the opposite pit
                self.board[opposite_pit] = 0  # Empties the opposite pit
                self.board[current_pit] = 0  # Empties the current pit

        elif self.current_player == 2 and current_pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1) and self.board[current_pit] == 1:
            opposite_pit = self.p1_mancala_index + self.p2_mancala_index - current_pit - 1  # Calculates the opposite pit
            if self.board[opposite_pit] > 0:
                self.board[self.p2_mancala_index] += self.board[opposite_pit] + 1  # Captures the stones in the opposite pit
                self.board[opposite_pit] = 0  # Empties the opposite pit
                self.board[current_pit] = 0  # Empties the current pit
            

        self.moves.append((self.current_player, pit + 1))  # Records the move
        self.current_player = 2 if self.current_player == 1 else 1  # Switches the current player
        
    
    def winning_eval(self):
        """
        Evaluates if the game board has reached the winning state.
        """
        result = 0  # Initializes the result to 0
        if all(self.board[pit] <= 0 for pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1)):
            for pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                self.board[self.p2_mancala_index] += self.board[pit]  # Player 2 captures all stones in their pits
                self.board[pit] = 0  # Empties the pits
                result = 1  # Sets the result to 1 indicating a win for player 2
        
        if all(self.board[pit] <= 0 for pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1)):
            for pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                self.board[self.p1_mancala_index] += self.board[pit]  # Player 1 captures all stones in their pits
                self.board[pit] = 0  # Empties the pits
                result = 1  # Sets the result to 1 indicating a win for player 1
        
        if not result:
            return 0  # If no player has won, returns 0

        res1= self.board[self.p1_mancala_index]  # Player 1's mancala stones
        res2= self.board[self.p2_mancala_index]  # Player 2's mancala stones
        
        if res1 > res2: return 1  # Player 1 wins
        if res2 > res1: return 2  # Player 2 wins
        return 3  # It's a tie
