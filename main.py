import mancala as m
import RandomPlayer as player


def play_game(player1, player2, game):
    playing = True
    while(playing):
        player1.play()
        player2.play()
        playing = False
        res = 1 # player 1 won
    return res


def main():
    
    player1, player2 = player.RandomPlayer(), player.RandomPlayer()

    for i in range(100):
        game = m.Mancala
        print(play_game(player1, player2, game))

        
if __name__ == "__main__":
    main()


