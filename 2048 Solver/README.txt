 Created an adversarial search agent to play the 2048-puzzle game


2048 is played on a 4x4 grid with numbered tiles which can slide up, down, left, or right. This game can be modeled as a two player game, in which the computer AI generates a 2- or 4-tile placed randomly on the board, and the player then selects a direction to move the tiles.
The tile-generating Computer AI of 2048 is not particularly adversarial as it spawns tiles irrespective of whether a spawn is the most adversarial to the user’s progress, with a 90% probability of a 2 and 10% for a 4(from GameManager.py). However, our Player AI will play as if the computer is adversarial since this proves more effective in beating the game. We will specifically use the expectiminimax algorithm.



•GameManager.py. This is the driver program that loads your Computer AI and Player AI and begins a game where they compete with each other. 
• Grid.py This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone()
• BaseAI.py This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different ”moves” for different AIs).
• ComputerAI.py. This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.
• IntelligentAgent.py. YThe IntelligentAgent class should inherit from BaseAI. The getMove() function to implement must return a number that indicates the player’s action. In particular, 0 stands for ”Up”, 1 stands for ”Down”, 2 stands for ”Left”, and 3 stands for ”Right”. This is where your player-optimizing logic lives and is executed. 