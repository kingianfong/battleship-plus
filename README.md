# battleship-plus
Project done for Cx1003 Introduction to Computational Thinking, where we had to make a game of battleships where the hits would affect a 3x3 area instead of a single point, and submarines could be placed below surface level, so there were two planes.

Our requirements were to create a functional game, and to impose a set of requirements for setting a password, and a password recovery system.

Enjoy!

gameplay: battleships.py<br>
demonstration: demo.py<br>
<br>
Sample account:<br>
Username: player1<br>
Password: Battleships1!<br>
<br>
On top of the requirements, additional features include:
+ Tracking of last login activity
+ Automatic saving of game progress
+ Hashing of login information including date of birth for password resets
+ Brute force deterrence by preventing multiple login attempts within 2 seconds if user is locked out
+ Customisable ship names and dimensions
+ System for preventing overlapping ships
+ Basic GUI (Matplotlib)
+ Colours of plots corresponding to what was hit or not (red for opponent ships, matching colours for ships hit)
+ Automated demonstration of the game (ships placed randomly, player hits systematically, opponent hits randomly)
<br>
Known issues:
+ plots do not close properly using IDLE on Mac OS
+ plot legends do not get aligned consistently
