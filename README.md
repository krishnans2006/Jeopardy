# Jeopardy

A Pygame version of Jeopardy that you can host!

## Configuration

To create the clues and answers for your game, edit the `main.py` file. You can customize the `jeopardy_board` and `double_jeopardy_board` variables to create your own board, using the example provided. This will let you customize the clues and answers for your game.

## Playing the game

To play the game, run `main.py`. You should have a terminal window and Pygame window open. The Terminal window is for the host's eyes only, while the Pygame window can be presented or shared to all the contestants. To start the game, the host will need to enter the list of contestants, separated by commas (example: `bob,joe,tim`).

The Pygame window will display player scores, the game board, clues, and more. Whenever a clue is chosen on the Pygame window, the answer to that clue will be displayed on the terminal window for the host to see. To score points for a clue, the host can click on specific places on the Pygame window to increase or decrease points. Clicking the top half of a player's box means they have answered the clue correctly; their points will increase and the game will return to the board view. Clicking the bottom half means they have incorrectly answered the clue; points will be deducted and the game will remain in the clue view for other players to answer. If time is up or every player has answered incorrectly, the host can click "No Answer" to move on.

Once the clues in the Jeopardy round have been depleted, the game will *automatically* move on to the Double Jeopardy round. The Final Jeopardy round is still being developed.