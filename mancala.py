import random
from random import choice
random.seed(109)

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        if self.board[pit-1]==0 or (pit>self.pits_per_player or pit<1):
            return False
        else:
            return True
        
    def random_move_generator(self):
        """
        Function to generate random valid moves with non-empty pits for the random player
        """
        
        # write your code here
        if self.current_player==1:
            options = [pit for pit in range(1,self.pits_per_player+1) if self.valid_move(pit)]
        else:
            options = [pit for pit in range(1,self.pits_per_player+1) if self.valid_move(pit)]
        return choice(options)
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """
        
        # write your code here
        if not self.valid_move(pit):
            print("INVALID MOVE")
        elif self.winning_eval():
            print("GAME OVER")
        elif self.current_player==1:
            print(f"Player 1 chose pit: {pit}")
            self.moves.append((1,pit))
            translated_pit = pit-1
            marbles_to_dist = self.board[translated_pit]
            curr_ind = translated_pit+1
            while marbles_to_dist>0:
                if curr_ind==self.p2_mancala_index: #Skip opponent mancala (And update index to restart)
                    curr_ind==0
                self.board[curr_ind]+=1 #Update marble count of pit by 1
                marbles_to_dist = marbles_to_dist-1 #Lose a marble
                curr_ind+=1 #Move to next pit
            self.board[translated_pit]=0
        elif self.current_player==2:
            print(f"Player 2 chose pit: {pit}")
            self.moves.append((2,pit))
            translated_pit = pit + self.pits_per_player
            marbles_to_dist = self.board[translated_pit]
            curr_ind = translated_pit+1
            while marbles_to_dist>0:
                if curr_ind==self.p1_mancala_index: #Skip opponent mancala
                    curr_ind+=1
                self.board[curr_ind]+=1 #Update marble count of pit by 1
                marbles_to_dist = marbles_to_dist-1 #Lose a marble
                curr_ind+=1 #Move to next pit
                if curr_ind==self.p2_mancala_index+1: #If out of bounds
                    curr_ind = 0 #Reset
            self.board[translated_pit]=0
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1
        return self.board
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        
        
        # write your code here
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        winning_state = [0]*self.pits_per_player
        if player_1_pits==winning_state or player_2_pits==winning_state:
            return True
        else:
            return False