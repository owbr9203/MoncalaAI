import mancala as m
import RandomPlayer as player


def play_game(player1: player, player2: player, game:m):
    playing = True
    curr_player = 1
    
    while(playing):
        status, turns = game.play(game.random_move_generator())
        if status < 0 :
            print("Failled")
            return
        
        if status > 0:
            print("Finished game")
            match status:
                case 1:
                    player1.num_wins += 1
                    player2.num_loss += 1
                    break
                case 2:
                    player1.num_loss += 1
                    player2.num_wins += 1
                    break
                case _:
                    player1.num_tie += 1
                    player2.num_tie += 1  
                    break   
        if curr_player == 1:

            player1.increment_turns(turns)
            curr_player = 2
        else:
            player2.increment_turns(turns)
            curr_player = 1
        
        # status, turns = game.play(game.random_move_generator())
        # if status < 0 :
        #     print("Failled")
        #     return
        # if status > 0:
        #     print("Finished game")
        #     break



def main():
    
    player1, player2 = player.RandomPlayer(), player.RandomPlayer()

    for i in range(100):
        
        game = m.Mancala()
        play_game(player1, player2, game)
        
        
        print("==============================player1==============================")
        player1.display_stats()
        print("==============================player2==============================")
        player2.display_stats()
        print(game.display_board())

        
if __name__ == "__main__":
    main()


