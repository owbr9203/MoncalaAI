import mancala as m
import RandomPlayer as player


def play_game(player1: player, player2: player, game:m):
    playing = True
    curr_player = 1
    turns = 0
    
    while(playing):
        status = game.play(game.random_move_generator())
        turns+=1
        if status < 0 :
            print("Failled")
            return turns
        
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
            curr_player = 2
        else:
            curr_player = 1
    return turns
        # status, turns = game.play(game.random_move_generator())
        # if status < 0 :
        #     print("Failled")
        #     return
        # if status > 0:
        #     print("Finished game")
        #     break



def main():
    
    player1, player2 = player.RandomPlayer(), player.RandomPlayer()
    total_turns = 0
    for i in range(100):
        
        game = m.Mancala()
        total_turns += play_game(player1, player2, game)
        
        
        print("==============================player1==============================")
        player1.display_stats()
        print("==============================player2==============================")
        player2.display_stats()
        print("=============================game stats============================")
        print("average turns per game: {}".format(total_turns/(i+1)))
        # print(game.display_board())

        
if __name__ == "__main__":
    main()


