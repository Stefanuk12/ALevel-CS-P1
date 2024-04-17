# Main

This is the initial entrypoint for the program, it asks the user which [`Puzzle`](./Puzzle.md) to load and keeps track of the score after every puzzle attempt.

## Source

```python
def Main():
    # Variables
    Again = "y"
    Score = 0

    # Keep the game going until the user does not want to play anymore
    while Again == "y":
        # Ask the user if they want to load a puzzle or use a standard one
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")

        # Load the puzzle from a file
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            # Load from a file
            # int cast rounds down to 38
            # Why `* 0.6`?
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))

        # Attempt the puzzle
        Score = MyPuzzle.AttemptPuzzle()

        # Print the score and ask the user if they want to play again
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()
```
