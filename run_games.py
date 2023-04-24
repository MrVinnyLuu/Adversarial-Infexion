# Script which automates the running of a specified number of games between two 
# given agents and calculates statistics regarding the outcomes of the games
# Usage: python3 run_games.py player1 player2 num_games

import sys, os, subprocess

player1 = sys.argv[1]
player2 = sys.argv[2]
num_games = int(sys.argv[3])

player1_win_count = 0
player2_win_count = 0
draw_count = 0

for i in range(num_games):
    # Run python3 -m referee player1 player2 > game_output.txt
    cmd_str = f"python3 -m referee {player1} {player2} > game_output.txt"
    subprocess.run(cmd_str, shell=True)
    
    # Read last line of game_output.txt to get winning player
    with open("game_output.txt") as f:
        for line in f:
            pass
        result_line = line

    if result_line.find("player 1") != -1:
        print(f"Game #{i}: winner is player 1")
        player1_win_count += 1
    elif result_line.find("player 2") != -1:
        print(f"Game #{i}: winner is player 2")
        player2_win_count += 1
    else:
        print(f"Game #{i}: draw")
        draw_count += 1

os.remove("game_output.txt")    # don't need this anymore

print("==============================================")
print(f"Number of games won by player 1: {player1_win_count}/{num_games}")
print(f"Number of games won by player 2: {player2_win_count}/{num_games}")
print(f"Number of draws: {draw_count}/{num_games}")

if player1_win_count > player2_win_count:
    print("Player 1 wins overall")
elif player2_win_count > player1_win_count:
    print("Player 2 wins overall")
else:
    print("Draw")