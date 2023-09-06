#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

# Import depedencies
import random

# BUG: This dependency is not used
import os

# The main entry point for the program
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

# The main game class
class Puzzle():
    # Constructor, takes in either one argument or two:
    # 1 Argument -> Load from file
    # 2+ Arguments -> Grid Size, Symbols Left, the rest are discarded/not used
    def __init__(self, *args):
        # Load from file
        if len(args) == 1:
            # Initialise all default private variables
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []

            # Load the puzzle with the grid size specified
            self.__LoadPuzzle(args[0])
        else:
            # Initialise some default private variables
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []

            # Create the grid, adds in blocked cells
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)

            # Add in the default allowed patterns and symbols
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

    # Loads the puzzle from a file
    def __LoadPuzzle(self, Filename):
        try:
            # Load the file in
            with open(Filename) as f:
                # Read the first line what has the number of symbols (Q, T, X)
                NoOfSymbols = int(f.readline().rstrip())

                # Add each symbol to the allowed symbols list
                for Count in range (1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                
                # Read the number of patterns
                NoOfPatterns = int(f.readline().rstrip())

                # Add each pattern to the allowed patterns list
                for Count in range(1, NoOfPatterns + 1):
                    # Splits into the symbol name and the symbol data
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
        
                # Read the grid size
                self.__GridSize = int(f.readline().rstrip())

                # Iterate through each possible cell
                for Count in range (1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")

                    # A blocked cell `@`
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        # Configure the cell and set the symbol
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])

                        # Make it so we cannot add those symbols to that cell
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)

                # The score for each symbol
                self.__Score = int(f.readline().rstrip())

                # How many symbols left
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    # The main game loop
    def AttemptPuzzle(self):
        # Used to break out of the loop
        Finished = False

        # Game loop
        while not Finished:
            # Show the puzzle currently, which each symbol in the cells
            self.DisplayPuzzle()

            # Display the score
            print("Current score: " + str(self.__Score))

            # Prompt the user for the row and columns, checking that each is an integer
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass

            # Prompt the user for a symbol
            Symbol = self.__GetSymbolFromUser()

            # Subtract from the amount of symbols they can place
            # BUG: Subtracts too early, should be after checking if the symbol is allowed
            self.__SymbolsLeft -= 1

            # Grab the cell related to the inputted row and column
            # BUG: No try-catch. This can fail if an invalid row column is added
            CurrentCell = self.__GetCell(Row, Column)

            # Make sure the symbol is allowed within this cell
            # BUG: Does not check if there already is a pattern here. Should be done during valid checking in column
            if CurrentCell.CheckSymbolAllowed(Symbol):
                # Set the symbol within the cell
                CurrentCell.ChangeSymbolInCell(Symbol)

                # Check if it matches any pattern
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)

                # Add the score on
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore

            # We ran out of symbols, the game is done
            if self.__SymbolsLeft == 0:
                Finished = True

        # Print the puzzle again
        print()
        self.DisplayPuzzle()
        print()

        # Return the total score
        return self.__Score

    # Grabs the cell associated with a row and column
    def __GetCell(self, Row, Column):
        # Attempt to index
        Index = ((self.__GridSize - Row) * self.__GridSize) + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            # Could not find the cell
            raise IndexError()

    # Checks if there is a match with any pattern
    # More analysis is needed to figure out how this works, how the pattern strings are generated, etc.
    # BUG: Returns true, even if there is an invalid match. For example, form a P shape then form a Q shape - this counts
    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    # Generate the pattern string from the 3x3 around
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()

                    # Check if it matches any pattern
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    # Grabs a valid symbol from the user
    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    # Creates a horizontal line with the size as double the grid size, plus two
    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    # Displays the puzzle
    # More analysis needed, AI helped with the comments on this one
    def DisplayPuzzle(self):
        print()
        # Print the column numbers
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()

        # Create a line
        print(self.__CreateHorizontalLine())

        # Printing the entire grid with symbols
        for Count in range(0, len(self.__Grid)):
            # Print the row number
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')

            # Print the symbol
            print("|" + self.__Grid[Count].GetSymbol(), end='')

            # Print the line
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

# Used to represent a pattern and check if it matches a pattern string
class Pattern():
    # Constructor, takes in the symbol to use and the pattern string
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    # Checks if the pattern matches the pattern string
    def MatchesPattern(self, PatternString, SymbolPlaced):
        # Check if the symbol placed is the same as the symbol we are checking for
        if SymbolPlaced != self.__Symbol:
            return False
        
        # Loop through each character in the pattern string
        for Count in range(0, len(self.__PatternSequence)):
            # Check if the pattern sequence is the same as the pattern string
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            # Errors = out of range
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    # Returns the pattern sequence
    def GetPatternSequence(self):
      return self.__PatternSequence

# Represents a cell within the grid
class Cell():
    # Constructor
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    # Grab the symbol, return `-` if empty
    def GetSymbol(self):
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    
    # Check if the cell is empty
    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    # Change the symbol in the cell
    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    # Check if the symbol is allowed within the cell
    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    # Add a symbol to the not allowed list
    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    # TODO: Update the cell. This could be asked about!
    def UpdateCell(self):
        pass

# Represents a blocked cell
class BlockedCell(Cell):
    # Constructor
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    # No symbol is allowed within this cell
    def CheckSymbolAllowed(self, SymbolToCheck):
        return False

# Runs the main function if this file is run
if __name__ == "__main__":
    Main()