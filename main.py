import mancala as m
import Player as player


def find_total_stones(game):
    total = 0
    for i in game.board:
        total += i
    return total


def play_rand_game(player1: player, player2: player, game:m):
    playing = True
    curr_player = 1
    turns = 0
    
    while(playing):
        status = game.play(game.random_move_generator())
        # print(status, "stones: ", find_total_stones(game))
        # game.display_board()
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

def play_game_alphabeta(player1: player, player2: player, game:m,depth: int=30):
    playing = True
    curr_player = 1
    turns = 0
    
    while(playing):
        status = game.play(game.alphabeta_search(depth))
        # print(status, "stones: ", find_total_stones(game))
        # game.display_board()
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

def play_game_alphabeta_rand(player1: player, player2: player, game:m, depth: int = 10):
    playing = True
    curr_player = 1
    turns = 0
    
    while(playing):
        if curr_player==1:
            status = game.play(game.alphabeta_search(depth))
        if curr_player==2:
            status = game.play(game.random_move_generator())
        # print(status, "stones: ", find_total_stones(game))
        # game.display_board()
        turns+=1
        if status < 0 :
            print("Failed")
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


def main():
    
    player1, player2 = player.Player(), player.Player()
    total_turns = 0
    for i in range(100):
        
        game = m.Mancala()
        total_turns += play_game_alphabeta_rand(player1, player2, game, 10)
        
        
        print("==============================player1==============================")
        player1.display_stats()
        print("==============================player2==============================")
        player2.display_stats()
        print("=============================game stats============================")
        print("average turns per game: {}".format(total_turns/(i+1)))
        # print(game.display_board())
        print(i)
    print(game.display_board())
        
if __name__ == "__main__":
    main()


