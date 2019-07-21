import matplotlib.pyplot as plt
import warnings
from board import *
from matplotlib import style

warnings.filterwarnings("ignore")  # ignores matplotlib warning
style.use("seaborn")  # sets style for plots

def colour(state_number):
    """ Returns the character corresponding to a specific colour. """
    colours = ['r', 'g', 'b', 'c', 'y', 'm']
    if state_number > len(ships_dict):
        state_number -= len(ships_dict) + 1  # ensures ships keep colour after hits
    return colours[state_number % len(colours)]

def display_boards(player_board, cpu_board):
    """ Shows the states of both players' boards. """
    plt.suptitle("CLOSE WINDOW TO CONTINUE", fontsize = 16)

    for (x, y, z), state_number in player_board.items():
        # plotting points on player board
        L = get_state(player_board, (x,y,z))
        C = colour(state_number)
        M = None
        
        if z == 1:
            plt.subplot(2,2,1)
            plt.title("Your surface")
        else:
            plt.subplot(2,2,2)
            plt.title("Your subsea")
            
        if "hit" in L:
            M = "x"
            if "empty" in L:
                C = "k"
        if state_number != 0:
                plt.scatter(x, y, label = L, color = C, marker = M)
            
    for (x, y, z), state_number in cpu_board.items():
        # plotting points on cpu board
        L = get_state(cpu_board, (x,y,z))
        M = "x"

        if z == 1:
            plt.subplot(2,2,3)
            plt.title("Opponent surface")
            
        else:
            plt.subplot(2,2,4)
            plt.title("Opponent subsea")
                    
        if "hit" in L:  # plots only if there are hits
            C = "k" 
            if "empty" not in L:
                L = "ship " + L.split()[1]  # renamed label
                C = "r"
            plt.scatter(x, y, label = L, color = C, marker = M)

    ticks = [i for i in range(11)]
    ticklabels = [str(i) for i in range(11)]

    for i in range(1,5):
        # adjusts setting for all subplots
        plt.subplot(2,2,i)
        plt.subplots_adjust(right = 0.8, wspace = 0.8, hspace = 0.45)
        plt.xlim(0, 11)
        plt.ylim(0, 11)
        plt.xticks(ticks, ticklabels)
        plt.yticks(ticks, ticklabels)
        plt.xlabel("x axis")
        plt.ylabel("y axis")
        plt.grid(True)
        handles, labels = plt.gca().get_legend_handles_labels()
        handle_list, label_list = [], []
        for handle, label in zip(handles, labels):
            if label not in label_list:
                handle_list.append(handle)
                label_list.append(label)
        plt.legend(handle_list, label_list,
                   bbox_to_anchor = (1.6, 0.3) )
    plt.show()

if __name__ == "__main__":
    for i in range(1):
        board1 = new_cpu_board()
        
        to_hit1 = (3, 3, 1)
        board1 = hit(board1, to_hit1)  # ensures hitting the same spot twice is okay
        to_hit2 = (5, 5, 0)
        board1 = hit(board1, to_hit2)
        
        display_boards(board1, board1)
