import mancala as m

class RandomPlayer():
    def __init__(self):
        """
        Initializes a Random Player that plays mancala
        """
        self.num_wins = 0
        self.num_loss = 0
        self.num_tie = 0
        self.turns = 0 # this is for each stone dropped into a pit
    
    def getAvgTurns(self):
        """
        Calculates the average turns the player takes by dividing turns by number of games
        """
        return self.turns/(self.num_wins+self.num_loss+self.num_tie)
    
    def getAvgWins(self):
        """
        Calculates the average wins by dividing wins by number of games
        """
        return self.num_wins/(self.num_wins+self.num_loss+self.num_tie)
    
    def getAvgLosses(self):
        """
        Calculates the average loss by dividing losses by number of games
        """
        return self.num_loss/(self.num_wins+self.num_loss+self.num_tie)
    
    def getAvgTies(self):
        """
        Calculates the average ties by dividing ties by number of games
        """
        return self.num_tie/(self.num_wins+self.num_loss+self.num_tie)
    
    def display_stats(self):
        print("win percentage:", self.getAvgWins())
        print("loss percentage:", self.getAvgLosses())
        print("tie percentage:", self.getAvgTies())
        print("average turns:", self.getAvgTurns())
        
        
    def increment_turns(self, num):
        self.turns += num
