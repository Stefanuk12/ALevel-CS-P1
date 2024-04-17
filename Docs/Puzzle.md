# Puzzle

Handles the operation of the game.

## `__init__`

Initialiser that takes different numbers of arguments depending on the mode it is running in:

### 1 Arg

Loads a puzzle from a file. Calls the [`__LoadPuzzle`](#__LoadPuzzle) method internally.

```python
# Initialise all default private variables
self.__Score = 0
self.__SymbolsLeft = 0
self.__GridSize = 0
self.__Grid = []
self.__AllowedPatterns = []
self.__AllowedSymbols = []

# Load the puzzle with the grid size specified
self.__LoadPuzzle(args[0])
```

### 2+ Args

First arg is the grid size, second arg is the symbols remaining. All other arguments are discarded.

#todo
