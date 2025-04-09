import mancala as m

class Player():
    def __init__(self):
        """
        Initializes a Random Player that plays mancala
        """
        self.num_wins = 0
        self.num_loss = 0
        self.num_tie = 0
    
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
