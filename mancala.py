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
        self.current_player = 1  # Initializes the current player to 1
        self.moves = []  # List to keep track of moves made
        self.p1_pits_index = [0, self.pits_per_player-1]  # Indexes for player 1's pits
        self.p1_mancala_index = self.pits_per_player  # Index for player 1's mancala
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]  # Indexes for player 2's pits
        self.p2_mancala_index = len(self.board)-1  # Index for player 2's mancala
        self.stones_per_pit = stones_per_pit
        
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
        Checks if the pit chosen by the current_player is a valid move. TAKES IN 0-index for where pit is on board
        """
        if self.current_player==1: #For P1
            if pit<0 or pit>=self.p1_mancala_index or self.board[pit]<=0: #If not one of P1's pits or empty...
                return False #Invalid
        else: #For P2
            if pit<=self.p1_mancala_index or pit>=self.p2_mancala_index or self.board[pit]<=0: #If not one of P2's pits or empty...
                return False #Invalid
        return True  # If all checks pass, the move is valid
        
    def valid_moves(self):
        pits = []
        if self.current_player == 1: #For P1
            for pit in range(self.p1_mancala_index): #For every P1 pit other than their mancala...
                if self.board[pit] > 0: #If that pit has stones in it
                    pits.append(pit) #Add to valid pits
        else: #For P2
            for pit in range(self.p1_mancala_index + 1, self.p2_mancala_index): #For every P2 pit other than their mancala...
                if self.board[pit] > 0: #If that pit has stones in it
                    pits.append(pit) #Add to valid pits
        return pits

    def random_move_generator(self):
        """
        Generates random valid moves with non-empty pits for the random player
        """
        
        pits = self.valid_moves()
        random_pit = random.randint(0, len(pits) - 1)
        return pits[random_pit] #Returns the random 0-index pit
    
    
    def play(self, pit):
        """
        Simulates a single move made by a specific player using their selected pit. Input is a 0-index pit.
        """
        
        if not self.valid_move(pit):
            print("INVALID MOVE")
            return -1 # Exits if the move is invalid
        

        
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
            
            self.board[current_pit] = 0  # Empties the current pit

            self.board[self.p1_mancala_index] += self.board[opposite_pit] + 1# Captures the stones in the opposite pit
            self.board[opposite_pit] = 0  # Empties the opposite pit
                

        elif self.current_player == 2 and current_pit in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1) and self.board[current_pit] == 1:
            opposite_pit = self.p2_mancala_index - current_pit - 1  # Calculates the opposite pit
            
            self.board[current_pit] = 0  # Empties the current pit
            self.board[self.p2_mancala_index] += self.board[opposite_pit] + 1 # Captures the stones in the opposite pit
            self.board[opposite_pit] = 0  # Empties the opposite pit


        self.moves.append((self.current_player, pit + 1))  # Records the move
        self.current_player = 2 if self.current_player == 1 else 1  # Switches the current player
        
        if self.winning_eval() != 0:
            # print("GAME OVER")
            return self.winning_eval() # Exits if the game is over
        
        
        return 0
        
    
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

    def utility(self,player=1):
        """
        Calculates the utility of an outcome for a player based on an integer representing a current state.
        """
        #TO-DO: See if this can/should be altered to work with difference in marbles rather than simply a winning state

        #Pros of just using terminal states: Easy, stops everything if a win is found
        #Pros of using difference in marbles: More complicated, may have to rework winning_eval or make a new method, could be much less expensive since a state of 32 to 4 may not be a winning state but is a good indicator of optimal play.
        if player==1:
            return self.board[self.p1_mancala_index] - self.board[self.p2_mancala_index]
        else:
            return self.board[self.p2_mancala_index] - self.board[self.p1_mancala_index]

    def max_value(self,default_state,alpha,beta,depth,player):
        """
        Calculates the maximum value the player can get out of this state.
        """
        terminal = default_state.winning_eval() #Calculates whether this state is a final state
        if terminal>0 or depth==0:
            return self.utility(player),-1 #Calculate the utility of this state for the player whose current turn it is
        value = -1*(self.pits_per_player * self.stones_per_pit*2 + 1)
        pit_to_return = -1
        pits = default_state.valid_moves() #Figure out what actions are possible (0-index)
        for pit in pits: #For every action...
            state = copy.deepcopy(default_state)#Clone the board state
            state.play(pit) #Play move on this hypothetical board
            pit_val, _ = self.min_value(state, alpha, beta,depth-1,player) #Determine value after making that move
            if pit_val>value: #If the worst move your opponent can force you into in this state is better than the worst move they can force you into in another state...
                value = pit_val #Select this value as our best value
                pit_to_return = pit #Bookmark the pit or action chosen
            if value>=beta: return value,pit_to_return #Prune if a value is found that is guaranteed to be chosen
            alpha = max(value,alpha) #Calculate new alpha if needed
        return value,pit_to_return #Return the value at this state
    
    def min_value(self,default_state,alpha,beta,depth,player):
        """
        Calculates the minimum value the player can get out of this state.
        """
        terminal = default_state.winning_eval() #Calculates whether this state is a final state
        if terminal>0 or depth==0:
            return self.utility(player),-1 #Calculate the utility of this state for the player whose current turn it is
        value = self.pits_per_player * self.stones_per_pit*2 + 1
        pit_to_return = -1
        pits = default_state.valid_moves() #Figure out what actions are possible (0-index)
        for pit in pits: #For every action...
            state = copy.deepcopy(default_state) #Clone the board state
            state.play(pit) #Play move on this hypothetical board
            pit_val, _ = self.max_value(state, alpha, beta,depth-1,player) #Determine value after making that move
            if pit_val<value: #If the best move the opponent can make in this state is worse than the best move they can make in another state...
                value = pit_val #Select this value as our best value
                pit_to_return = pit #Bookmark the pit or action chosen
            if value<=alpha: return value, pit_to_return #Prune if a value is found that is guaranteed to be chosen
            beta = min(value,beta) #Calculate new beta if needed
        return value, pit_to_return #Return the value at this state


    def alphabeta_search(self,depth,player=1):
        """
        Performs AlphaBeta on the Mancala game.
        """
        #TO-DO: Decide whether to keep this as a member of the Mancala class OR make it separate
        #Pros of keeping it in: Less work and difference may be marginal
        #Pros of keeping it separate: More work but difference may be craazyyy
        beta = self.pits_per_player * self.stones_per_pit*2 + 1
        alpha = -beta
        state = copy.deepcopy(self)
        value,pit = self.max_value(state,alpha,beta,depth,player)
        return pit