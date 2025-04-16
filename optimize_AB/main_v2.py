import alpha_beta_optimized as AB_NEW
import mancala_v3 as m
import Player as player
import time
from multiprocessing import Pool


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
        
        ab_obj = AB_NEW.AB_OPTIMIZED(game)
        
        if curr_player==1:
            status = game.play(ab_obj.alphabeta_search(depth), game.board, 1)
        if curr_player==2:
            status = game.play(game.random_move_generator(game.board, 2),game.board, 2)
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
    
    
    start_time = time.time()
    
    player1, player2 = player.Player(), player.Player()
    total_turns = 0
    
    
    for i in range(3):
        
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
    # print(game.display_board())
    
    print("time: ", time.time() - start_time)


def play_game_and_update_stats(args):
        game, depth = args
        # Create new player instances for each process
        p1, p2 = player.Player(), player.Player()
        turns = play_game_alphabeta_rand(p1, p2, game, depth)
        return {
            'turns': turns,
            'p1_wins': p1.num_wins,
            'p1_losses': p1.num_loss,
            'p1_ties': p1.num_tie,
            'p2_wins': p2.num_wins,
            'p2_losses': p2.num_loss,
            'p2_ties': p2.num_tie
        }
        
def new_main():
    start_time = time.time()

    num_games = 100
    depth = 12
    
    # Create game instances and depth parameters
    games = [m.Mancala() for _ in range(num_games)]
    depths = [depth] * num_games
    args = list(zip(games, depths))

    # Create a pool and run the games
    with Pool() as p:
        results = p.map(play_game_and_update_stats, args)

    # Aggregate results
    total_turns = 0
    total_p1_wins = 0
    total_p1_losses = 0
    total_p1_ties = 0
    total_p2_wins = 0
    total_p2_losses = 0
    total_p2_ties = 0

    for i, result in enumerate(results):
        total_turns += result['turns']
        total_p1_wins += result['p1_wins']
        total_p1_losses += result['p1_losses']
        total_p1_ties += result['p1_ties']
        total_p2_wins += result['p2_wins']
        total_p2_losses += result['p2_losses']
        total_p2_ties += result['p2_ties']

        print(f"\nGame {i+1} Results:")
        print("==============================player1==============================")
        print(f"Wins: {total_p1_wins}, Losses: {total_p1_losses}, Ties: {total_p1_ties}")
        print("==============================player2==============================")
        print(f"Wins: {total_p2_wins}, Losses: {total_p2_losses}, Ties: {total_p2_ties}")
        print("=============================game stats============================")
        print(f"Average turns per game: {total_turns/(i+1)}")

    
    print("time: ", time.time() - start_time)


if __name__ == "__main__":
    # main()
    new_main()


