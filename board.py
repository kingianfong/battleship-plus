import pickle
import random
from settings import ships
ships_dict = ships()

def empty_board():
    """ Returns an empty 10 by 10 by 2 board as a dictionary. """
    board = {}
    for i in range(1, 11):
        for j in range(1, 11):
            for k in range(0, 2):
                board[(i,j,k)] = 0
    return board

def hit(board, coordinates):
    """ Returns a board after it is hit at a given coordinate. """
    x, y, z = coordinates
    ship_count = len(ships_dict)
    
    for i in (x-1, x, x+1):
        for j in (y-1, y, y+1):
            try:
                if board[(i,j,z)] in range(ship_count + 1):
                    # if grid not not alraedy hit, increase 
                    board[(i,j,z)] += (ship_count + 1)
            except:
                pass
    return board

def get_state(board, coordinates):
    """ Returns the state of the given coordinate on a given board. """
    x, y, z = coordinates
    board_states = {0: "empty"}
    ship_count = len(ships_dict)
    
    for i in range(ship_count):
        # generates board states based on available ships
        board_states[i + 1] = list(ships_dict.keys())[i]
    for i in range(ship_count + 1):
        # generates board states for each state after it gets hit
        board_states[i + ship_count + 1] = board_states[i] + " (hit)"

    board_states = dict(sorted(board_states.items()))  # sorts dictionary by keys
    state_number = board[coordinates]
    state = board_states[state_number]
    return state

def save_boards(username, player_board, cpu_board):
    """ Saves two boards as a .pickle file named as username. """
    filename = username + ".pickle"
    boards = (player_board, cpu_board)
    with open(filename, "wb") as file_object:
        pickle.dump(boards, file_object)

def load_boards(username):
    """ Returns two boards saved under given username. """
    filename = username + ".pickle"
    with open(filename, "rb") as file_object:
        player_board, cpu_board = pickle.load(file_object)
    return player_board, cpu_board

def valid_placement(board, ship_type, x, y, depth, orient):
    """ Returns a bool based on board, ship type, coordinates and orientation. """
    ship_length = ships_dict[ship_type]
    
    if orient == "H":
        for i in range(ship_length):
            if x + i > 10:
                return False
            
            if board[(x + i, y, depth)] != 0:
                return False
            
    elif orient == "V":
        for i in range(ship_length):
            if y + i > 10:
                return False
            
            if board[(x, y + i, depth)] != 0:
                return False
    return True

def add_ship(board, ship_type, x , y, depth, orient):
    """ Returns a board with a ship placed using board, ship type, coordinates and orientation. """
    ship_length = ships_dict[ship_type]
    identifier = list(ships_dict.keys()).index(ship_type) + 1  # cprresponds to states
    
    if orient == "H":
        for i in range(ship_length):
            board[(x+i,y,depth)] = identifier
            
    else:
        for i in range(ship_length):
            board[(x,y+i,depth)] = identifier
    return board

def new_cpu_board():
    """ Returns a board with ships randomly placed. """
    board = empty_board()
    
    for ship_type in ships_dict.keys():
        ship_length = ships_dict[ship_type]
        identifier = list(ships_dict.keys()).index(ship_type) + 1  # corresponds to states
        depth = 1
        
        valid = False
        while not valid :
            # randomly tries coordinates and orientations until ship placement is valid
            orient = random.choice(["V","H"])
            if ship_type == "submarine":
                depth = random.randint(0,1)
            x = random.randint(1,10) 
            y = random.randint(1,10)
            
            valid = valid_placement(board, ship_type, x, y, depth, orient)
        board = add_ship(board, ship_type, x, y, depth, orient)
    return board

def get_coordinate(axis, upper = 10):
    """ Returns an integer between 1 to an upper limit using user input. """
    prompt = "Enter {} coordinate\n1 to {}: ".format(axis, upper)
    valid_coordinates = [str(i+1) for i in range(upper)]
    attempts = 3
    while attempts > 0:
        attempts -= 1
        coordinate = input(prompt)
        if coordinate in valid_coordinates:
            coordinate = int(coordinate)
            break
        else:
            print("1 to {} only".format(upper))
    else:
        coordinate = random.randint(1,10)
        print("Using {}".format(coordinate))
    return coordinate

def get_depth():
    """ Returns depth (0 or 1) using user input. """
    attempts = 3
    while attempts > 0:
        attempts -= 1
        depth = input("Enter depth\n'1' for surface, '0' for subsurface': ")
        if depth == '0' or depth == '1':
            depth = int(depth)
            break
        else:
            print("'0' or '1' only")
    else:
        depth = random.randint(1,10)
        print("Using {}".format(depth))
    return depth

def get_orient():
    """ Returns orientation ('V' or 'H') using user input. """
    attempts = 3
    while attempts > 0:
        attempts -= 1
        orient = input("Enter orientation\n'H' for horizontal, 'V' for vertical: ").upper()
        if orient == 'V' or orient == 'H':
            break
        else:
            print("'V' or 'H' only")
    else:
        orient = random.choice(["V","H"])
        print("Using {}".format(orient))
    return orient

def new_player_board():
    """ Returns a board with ships placed using user input. """
    board = empty_board()
    
    for ship_type in list(ships_dict.keys()):
        ship_length = ships_dict[ship_type]
        identifier = list(ships_dict.keys()).index(ship_type) + 1  # corresponds to states
        
        valid = False
        while not valid:
            print("\nPlacing {}...".format(ship_type))
            depth = 1
            x_upper = y_upper = 10
            orient = get_orient()
            
            if orient == 'H':
                x_upper -= ship_length
            else:
                y_upper -= ship_length
                
            if ship_type == "submarine":
                depth = get_depth()
                
            x = get_coordinate("x", x_upper)
            y = get_coordinate("y", y_upper)

            valid = valid_placement(board, ship_type, x, y, depth, orient)
            if valid == False:
                print("\nInvalid {} placement, please try again\n".format(ship_type))
        else:
            board = add_ship(board, ship_type, x, y, depth, orient)
            print("\nPlaced {}\n".format(ship_type))
            
    return board
        
if __name__ == "__main__":
    import os
    
    def test_boards():
        """ Checks boards and hits by making random boards, hitting them and comparing hit counts. """
        board1 = new_cpu_board()  # board 1 is has randomly allocated ships
        board2 = board1.copy()  # board 2 is a copy with same ships
        
        to_hit1 = (3, 3, 1)
        board1 = hit(board1, to_hit1)  # board 1 has a 3x3 hit
        board1 = hit(board1, to_hit1)  # ensures hitting the same spot twice is okay
        
        hits = misses = floating_ships = board1_non_zero = total_ships = 0

        # counting non-zero states, hits, misses, and floating ships on board1
        for i, j in board1.items():
            state = get_state(board1, i)
            if j != 0:
                board1_non_zero += 1
                if "hit" in state:
                    if "empty" not in state:
                        hits += 1
                    else:
                        misses += 1
                else:
                    floating_ships += 1

        # counting non-zero states on board2 which has not been hit
        for i, j in board2.items():
            state = get_state(board1, i)
            if j != 0:
                total_ships += 1

        # checking correct number of ships
        if total_ships != sum(list(ships_dict.values())):
            print("WRONG NUMBER OF SHIPS")
            print(f"b2 all non-0: {total_ships}")
            for i, j in board2.items():
                if j != 0:
                    print(i, get_state(board2, i))
                    
        # checking correct number of hits
        if board1_non_zero == floating_ships + misses + hits:
            print("HITS OKAY")
        else:
            print("WRONG NUMBER OF HITS")
            print(f"b1 ship hits: {hits}")
            print(f"b1 all non-0: {board1_non_zero}")
            for i, j in board1.items():
                if j != 0:
                    print(i, get_state(board1, i))
                    
    def test_saves():
        """ Checks if boards are saved and loaded correctly by checking every combination. """
        username = "testuser"
        board1 = new_cpu_board()
        board2 = board1.copy()
            
        to_hit1 = (3, 3, 1)
        board1 = hit(board1, to_hit1)
        
        save_boards(username, board1, board2)
        board3, board4 = load_boards(username)
        test12 = board1 == board2
        test13 = board1 == board3
        test14 = board1 == board4
        test23 = board2 == board3
        test24 = board2 == board4
        
        if ( test12 == test14 == test23 == (not test13) == (not test24) ):
            print("SAVES OKAY")
        else:
            print("WRONG SAVES")
        os.remove(username + ".pickle")
            
    for i in range(10):
        test_boards()
        test_saves()

        
