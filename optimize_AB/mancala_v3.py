import random
from random import choice
import time
import copy
random.seed(time.process_time_ns())  # Seeds the random number generator for reproducibility

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        Initializes the Mancala game with specified number of pits and stones per pit.
        """
        self.pits_per_player = pits_per_player  # Sets the number of pits per player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2  # Number of players in the game
        # self.current_player = 1  # Initializes the current player to 1
        self.moves = []  # List to keep track of moves made
        self.p1_pits_index = [0, self.pits_per_player-1]  # Indexes for player 1's pits
        self.p1_mancala_index = self.pits_per_player  # Index for player 1's mancala
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]  # Indexes for player 2's pits
        self.p2_mancala_index = len(self.board)-1  # Index for player 2's mancala
        self.stones_per_pit = stones_per_pit
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0  # Sets player 1's mancala to 0
        self.board[self.p2_mancala_index] = 0  # Sets player 2's mancala to 0

    def display_board(self, board, current_player):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]  # Extracts player 1's pits
        player_1_mancala = board[self.p1_mancala_index]  # Extracts player 1's mancala
        player_2_pits = board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]  # Extracts player 2's pits
        player_2_mancala = board[self.p2_mancala_index]  # Extracts player 2's mancala

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
        turn = 'P1' if current_player == 1 else 'P2'  # Determines whose turn it is
        print('Turn: ' + turn)  # Displays whose turn it is
        
    def valid_move(self, pit, board, current_player):
        """
        Checks if the pit chosen by the current_player is a valid move. TAKES IN 0-index for where pit is on board
        """
        if current_player==1: #For P1
            if pit<0 or pit>=self.p1_mancala_index or board[pit]<=0: #If not one of P1's pits or empty...
                return False #Invalid
        else: #For P2
            if pit<=self.p1_mancala_index or pit>=self.p2_mancala_index or board[pit]<=0: #If not one of P2's pits or empty...
                return False #Invalid
        return True  # If all checks pass, the move is valid
        
    def valid_moves(self, board, current_player):
        if current_player == 1: #For P1
            return [pit for pit in range(self.p1_mancala_index) if board[pit] > 0] #For every P1 pit other than their mancala...
        else: #For P2
            return [pit for pit in range(self.p1_mancala_index + 1, self.p2_mancala_index) if board[pit] > 0] #For every P2 pit other than their mancala...

    def random_move_generator(self, board, current_player):
        """
        Generates random valid moves with non-empty pits for the random player
        """
        
        pits = self.valid_moves(board, current_player)
        random_pit = random.randint(0, len(pits) - 1)
        return pits[random_pit] #Returns the random 0-index pit
    
    def valid_move_helper(self,board,current_player):
        """
        Given a board and input gets valid moves and asks player to make one of those moves
        """
        valid = False
        pits = self.valid_moves(board,current_player)
        translated_pits = [pit+1 if current_player==1 else (pit-self.p2_pits_index[0]+1) for pit in pits]
        print(f"Available actions for P{current_player}:")
        for pit in translated_pits:
            print(f"Pit {pit}")
        while not valid:
            action = int(input("Choose a pit: "))
            if action in translated_pits:
                valid = True
                if current_player==1:
                    return action-1
                else:
                    return action+self.p2_pits_index[0]-1
            else:
                print("Not a valid pit, try again.")
    
    def _calculate_opposite_pit(self, current_pit):
        """Helper method to calculate the opposite pit index"""
        return self.p2_mancala_index - current_pit - 1

    def play(self, pit, board, current_player):
        """
        Simulates a single move made by a specific player using their selected pit. Input is a 0-index pit.
        """
        if not self.valid_move(pit, board, current_player):
            return -1  # Exits if the move is invalid
        
        stones = board[pit]  # Number of stones in the selected pit
        board[pit] = 0  # Empties the selected pit
        
        # Calculate the number of full cycles and remaining stones
        board_length = len(board)
        full_cycles = stones // (board_length - 1)  # -1 to account for skipping opponent's mancala
        remaining_stones = stones % (board_length - 1)
        
        # Distribute stones in bulk for full cycles
        if full_cycles > 0:
            for i in range(board_length):
                if (current_player == 1 and i == self.p2_mancala_index) or \
                   (current_player == 2 and i == self.p1_mancala_index):
                    continue
                board[i] += full_cycles
        
        # Distribute remaining stones
        current_pit = pit
        for _ in range(remaining_stones):
            current_pit = (current_pit + 1) % board_length
            if (current_player == 1 and current_pit == self.p2_mancala_index) or \
               (current_player == 2 and current_pit == self.p1_mancala_index):
                current_pit = (current_pit + 1) % board_length
            board[current_pit] += 1

        # Check for capture
        if board[current_pit] == 1:  # Only check if we ended with 1 stone
            if current_player == 1 and self.p1_pits_index[0] <= current_pit <= self.p1_pits_index[1]:
                opposite_pit = self._calculate_opposite_pit(current_pit)
                captured_stones = board[opposite_pit] + 1
                board[self.p1_mancala_index] += captured_stones
                board[current_pit] = 0
                board[opposite_pit] = 0
            elif current_player == 2 and self.p2_pits_index[0] <= current_pit <= self.p2_pits_index[1]:
                opposite_pit = self._calculate_opposite_pit(current_pit)
                captured_stones = board[opposite_pit] + 1
                board[self.p2_mancala_index] += captured_stones
                board[current_pit] = 0
                board[opposite_pit] = 0

        self.moves.append((current_player, pit + 1))
        current_player = 2 if current_player == 1 else 1
        
        return self.winning_eval(board, current_player) if self.winning_eval(board, current_player) != 0 else 0
        
    
    def winning_eval(self, board, current_player):
        """
        Evaluates if the game board has reached the winning state.
        """
        result = 0  # Initializes the result to 0
        if all(board[pit] <= 0 for pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1)):
            for pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                board[self.p2_mancala_index] += board[pit]  # Player 2 captures all stones in their pits
                board[pit] = 0  # Empties the pits
                result = 1  # Sets the result to 1 indicating a win for player 2
        
        if all(board[pit] <= 0 for pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1)):
            for pit in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                board[self.p1_mancala_index] += board[pit]  # Player 1 captures all stones in their pits
                board[pit] = 0  # Empties the pits
                result = 1  # Sets the result to 1 indicating a win for player 1
        
        if not result:
            return 0  # If no player has won, returns 0

        res1= board[self.p1_mancala_index]  # Player 1's mancala stones
        res2= board[self.p2_mancala_index]  # Player 2's mancala stones
        
        if res1 > res2: return 1  # Player 1 wins
        if res2 > res1: return 2  # Player 2 wins
        return 3  # It's a tie