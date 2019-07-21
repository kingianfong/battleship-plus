import random
import os
from accounts import select_user
from board import *
from gui import *

def load_game():
    """ Returns True if user wants to load a game, returns False otherwise. """
    while True:
        # checks if user wants to load a saved file
        load = input("Contiunue previous game? 'y' or 'n' ")
        if load.lower() == 'y':
            return True
        elif load.lower() == 'n':
            return False
        else:
            print("\nPlease enter 'y' or 'n' only")

def player_turn(cpu_board):
    """ Returns opponent's board after it takes a hit from user. """
    
    print("Your turn!")
    x = get_coordinate('x')
    y = get_coordinate('y')
    z = get_depth()

    to_hit = (x, y, z)
    cpu_board =  hit(cpu_board, to_hit)

    return cpu_board
    
def random_coordinates():
    """ Returns random coordinates for CPU targeting. """
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    z = random.randint(0, 1)
    return (x, y, z)

def cpu_turn(player_board):
    """ Returns player's board after hitting it. """

    to_hit = random_coordinates()
    while "hit" in get_state(player_board, to_hit):
        # generates new set of coordinates if initial location already hit
        to_hit = random_coordinates()

    x, y, z = to_hit
    
    if z == 0:
        depth = "subsea"
    else:
        depth = "surface"
    
    print(f"Opponent hit: {format(depth, '7')}, X:{format(x, '3,d')}, Y:{format(y, '3,d')}")

    player_board = hit(player_board, to_hit)
    return player_board

def all_ships_hit(board):
    """ Returns True if all ships hit, returns False otherwise. """
    for i, j in board.items():
        state = get_state(board, i)
        
        if "empty" not in state and "hit" not in state:
            # checks for locations without "empty" and "hit"
            return False
    return True

def new_game():
    """ Returns True if user wants to start a new game, returns False otherwise. """
    global counter
    # counter for cpu1_turn
    counter = 0  # resets counter

    while True:
        # checks if user wants to load a saved file
        new = input("Start new game? 'y' or 'n' ")
        if new.lower() == 'y':
            return True
        elif new.lower() == 'n':
            return False
        else:
            print("\nPlease enter 'y' or 'n' only")
        
def gameplay(username):
    """ Plays the game under the username given. """
    save_file = username + ".pickle"
    save_file_exists = os.path.isfile(save_file)
    
    if save_file_exists and load_game():
        # loads saved game if save file exist and user wants to load game
        player_board, cpu_board = load_boards(username)
    else:
        # creates new boards if no saved file exists
        player_board, cpu_board = new_player_board(), new_cpu_board()
    
    game_over = False
    while not game_over:
        # loops whenever the game is not over
        display_boards(player_board, cpu_board)
        save_boards(username, player_board, cpu_board)

        # player's turn
        cpu_board = player_turn(cpu_board)
        if all_ships_hit(cpu_board):
            print("Congratulations, you win!")
            game_over = True
            continue

        # cpu's turn
        player_board = cpu_turn(player_board)
        if all_ships_hit(player_board):
            print("Game over")
            game_over = True
            continue
        
    else:
        # displays board and removes saved game
        display_boards(player_board, cpu_board)
        os.remove(save_file)

def demonstration():
    """ Demonstrates the game with cpu vs cpu without displaying board. """    
    # variables for systematic hits from demo_cpu
    x = y = [2, 5, 8, 10]
    z = [1, 0]
    # list comprehension sequence chosen to hit surface first
    hitlist = [ (i, j, k) for k in z for j in y for i in x ]
                
    def demo_cpu_turn(player_board):
        """ Returns player's board after hitting it (systematic). """
        to_hit = hitlist.pop(0)  # uses and removes the first item in the list
        x, y, z = to_hit
        
        if z == 0:
            depth = "subsea"
        else:
            depth = "surface"
        
        print(f"Opponent hit: {format(depth, '7')}, X:{format(x, '3,d')}, Y:{format(y, '3,d')}")

        player_board = hit(player_board, to_hit)
        return player_board
    
    username = "testuser"
    save_file = username + ".pickle"
    save_file_exists = os.path.isfile(save_file)

    if save_file_exists and load_game():
        # loads saved game if save file exist and user wants to load game
        player_board, cpu_board = load_boards(username)
    else:
        # creates new boards if no saved file exists
        player_board, cpu_board = new_cpu_board(), new_cpu_board()
    
    game_over = False
    while not game_over:
        # loops whenever the game is not over
        save_boards(username, player_board, cpu_board)

        # player's turn
        cpu_board = demo_cpu_turn(cpu_board)
        if all_ships_hit(cpu_board):
            print("Congratulations, you win!")
            game_over = True
            continue

        # cpu's turn
        player_board = cpu_turn(player_board)
        if all_ships_hit(player_board):
            print("Game over")
            game_over = True
            continue
        
    else:
        # displays board and removes saved game
        os.remove(save_file)
        display_boards(player_board, cpu_board)
    if new_game():
        demonstration()
        
def main():
    username = select_user()
    gameplay(username)
    if new_game():
        gameplay(username)
        
if __name__ == "__main__":
    main()
##    demonstration()
