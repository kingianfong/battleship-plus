"""
This file contains the following settings for the game.

1. Ship names and lengths
2. User data file name

Saved files do not work across different settings for ships.
"""

def ships():
    """ Returns a dictionary with the ship names and lengths. """
    ships_dict = {"carrier": 4, "submarine": 3, "frigate": 3}
    return ships_dict

def user_data_file():
    """ Returns the name of the save file. """
    return "userdata.csv"
