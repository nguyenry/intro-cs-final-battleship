# intro-cs-final-battleship
Text-based board game of Battleship w/ AI functionality (Final Project for CSCI 005 - Introduction to Computer Science at Harvey Mudd College)

We have a Board class representing a game of Battleship. The board is a traditional 10x10 playing field with 5 ships to place: Aircraft Carrier (5 spaces), Battleship (4 spaces), Cruiser (3 spaces), Submarine (3 spaces), and Destroyer (2 spaces).

There are 5 ways to run the game. Two of the modes are meant for easy testing ("Grader" mode) where you can see your opponent's set and compete against another player or the smart AI. The other three modes are more traditional where you can play against a random AI, against another player, or against a smarter AI without seeing their board.

The AI shoots randomly until it hits a ship, replacing the spot on the board to "X." Once it hits a ship, it fires around that spot to find more X's. My current AI favors ships that are horizontal and takes more steps for vertical ships. It also creates a "border" of shots around a region of ships while trying to check for more X's, which may be excessive but is actually a pretty sound strategy that I may or may not have lost against.

Thoughts for the future:
I really want to improve my AI so that it notices when there's a vertical ship or a horizontal ship. That way, it could just fire some shots around a singular X and then trace a ship vertically or horizontally. Right now, the AI shoots clockwise around an X and happens to travel vertically over time to find the ship. I'd also like to improve my host game functions so that they will have you keep inputting if you input the wrong datatype (e.g., putting a integer for the column when you should input a character between A-J).
