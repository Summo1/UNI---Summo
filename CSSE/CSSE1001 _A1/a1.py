# DO NOT modify or add any import statements
from support import *

# Name: Thomas Summerton
# Student Number: 49606782
# Favorite Marsupial: Rock Wallaby
# -----------------------------------------------------------------------------

# Define your functions here (start with def num_hours() -> float)


def num_hours() -> float:
    """
    returns number of hours worked on the project
    >>> num_hours()
    15.5
    """

    return 15.5

def move_to_index(cellID:str) -> tuple[int,int]:

    """
        returns the (row, column) index of a coordinate based on a letter (a-z) and numerical input
        >>> move_to_index("A5")
        (0,4)
    """

    rowIndex = ord(cellID[0].upper()) - 65 # converting letter to numerical order and then to relevant coord
    columnIndex = int(cellID[1:len(cellID)+1]) - 1 #converting everything after the letter as though it was one number, down a number for index

    numericID = (rowIndex, columnIndex)
    return numericID


def move_to_numeric(numericID:tuple[int,int]) -> str:

    """
        returns the alphanumerical cellID of a coordinate based on a (row, column) input
        >>> move_to_index(0,4)
        'A5'
    """
    #converting first number to a letter and then second number up by one
    cellID = str(chr(numericID[0] + 65)) + str(numericID[1] + 1) 
        
    return cellID

def generate_empty_board(size:int) -> list[list[str]]:

    """
        Generates an empty playing board with a specified number of rows. The rows are filled with '+' to signify an empty place
        Precondition:
            Size will not be negative
        >>> generate_empty_board(3)
        [['+', '+', '+'], ['+', '+', '+'], ['+', '+', '+']]
    """
    
    emptyBoard = []
    for rowFiller in range(size): # filling in '+'
        emptyBoard.append([])
        for columnFiller in range(size):
            emptyBoard[rowFiller].append('+')
            
    return emptyBoard

def generate_initial_board():

    """
        Generates an empty board of length 8 with the four centre squares filled with 'O' and 'X' in a cross pattern
        >>> generate_initial_board()
        [['+', '+', '+', '+', '+', '+', '+', '+'], ['+', '+', '+', '+', '+', '+', '+', '+'], ['+', '+', '+', '+', '+', '+', '+', '+'], ['+', '+', '+', 'O', 'X', '+', '+', '+'], ['+', '+', '+', 'X', 'O', '+', '+', '+'], ['+', '+', '+', '+', '+', '+', '+', '+'], ['+', '+', '+', '+', '+', '+', '+', '+'], ['+', '+', '+', '+', '+', '+', '+', '+']]

    """

    playBoard = generate_empty_board(8) 

    # filling in the centre four squares as desired

    playBoard[3][3] = 'O'
    playBoard[4][4] = 'O'
    playBoard[3][4] = 'X'
    playBoard[4][3] = 'X'
    
    return playBoard




def check_winner(board:list[list[str]]) -> str:

    """
        Returns the piece (X,O) that occurs the most frequently within a given board. Returns nothing if the quantity of each is equal

        >>> check_winner([[X,X,O],[1,2,X]])
        'X'
    """
    #tallies

    counterX = 0
    counterO = 0
    for rowCounter in range(len(board)):
        for item in board[rowCounter]:
            # adding to X and O based on found characters
            if item == 'X': 
                counterX += 1
            elif item == 'O':
                counterO += 1
    # logic to determin winner
    if counterX > counterO:
        return 'X'
    elif counterX < counterO:
        return 'O'
    else:
        return ''
                
def get_intermediate_locations(position: tuple[int, int], new_position: tuple[int, int]) -> list[tuple[int, int]]:

    """
        Returns a list of indexes (row, column) that are in a straight line between two points
        Lines can be vertical, horizontal or, diagonal
        Returns an empty list if the coordinates do not have lines between them or they are adjacent coordinates

        >>> get_intermediate_locations((0,0), (0,3))
        [(0, 1), (0, 2)]

        >>> get_intermediate_locations((0,1), (4,1))
        [(1, 1), (2, 1), (3, 1)]

        >>> get_intermediate_locations((0,0), (-3,3))
        [(-1, 1), (-2, 2)]

        >>> get_intermediate_locations((1,1), (2,2))
        []

        >>> get_intermediate_locations((1,1), (6,5))
        []
    """



    list_of_locations = []

    # direction to account for negatives [row direction, column direction]
    direction = [0,0]
    
    
    if position == new_position: # Returns nothing if the same coord is start and end position
        return list_of_locations

    elif position[0] == new_position[0]: #If positions share a row then checks the coords between them horizontally
        direction = [0, (new_position[1] - position[1])//abs(new_position[1] - position[1])]
        for x in range(0, new_position[1] - position[1], direction[1]):
            list_of_locations.append((position[0], position[1] + x))
        list_of_locations.remove(list_of_locations[0])
        return list_of_locations

    elif position[1] == new_position[1]: #If positions share a column then checks the coords between them vertically
        direction = [(new_position[0] - position[0])//abs(new_position[0] - position[0]), 0]
        for x in range(0, new_position[0] - position[0], direction[0]):
            list_of_locations.append((position[0] + x, position[1]))
        list_of_locations.remove(list_of_locations[0])
        return list_of_locations

    #diagonal checking

    elif (new_position[0] - position[0])/(new_position[1] - position[1]) == 1 or (new_position[0] - position[0])/(new_position[1] - position[1]) == -1: #finds if the line between two coords has gradient of 1
        direction = [(new_position[0] - position[0])//abs(new_position[0] - position[0]), (new_position[1] - position[1])//abs(new_position[1] - position[1])] #determines the direction vertically and horizontally that cells will be iterated through 
        
        temp_list = []
        for vert in range(0, new_position[0] - position[0], direction[0]): # vertical coordinate of coords on diagonal
            temp_list.append([position[0] + vert])
        for horiz in range(0, new_position[1] - position[1], direction[1]): # horizontal coordinate of coords on diagonal
            temp_list[horiz].append(position[1] + horiz)
        for a in range(len(temp_list)):
            list_of_locations.append((temp_list[a][0],temp_list[a][1]))

        list_of_locations.remove(list_of_locations[0])
        return list_of_locations
    
    else:
        return list_of_locations

    
def determine_other_player(piece:str):

    """
        Determines the other player's pieces based on the inputted pieces
        Precondition:
            Only 'X' and 'O' will be input
        >>> determine_other_player('X')
        'O'
        >>> determine_other_player('O')
        'X'
    """


    other_piece = ""
    # if X -> O if O -> X
    if piece == "X":
        other_piece = "O"
    elif piece == "O":
        other_piece = "X"
    return other_piece



def generate_dashed_row(width:int) -> str:

    """
        Generates a dashed row based on the width of a board for displaying a board. 2nd and final rows

        >>> generate_dashed_row(4)
        '  ----'
    """

    dashedRow = '  ' # generates a row of dashes a given distance wide that has a 2 column space for the formatting specifications
    for w in range(width):
        dashedRow += '-'
    return dashedRow

def generate_header_rows(width:int) -> str:

    """
    Generates a header row for displaying a board that has the column numbers and a dashed outlining row

    >>> generate_header_rows(4)
    '  1234\n  ----\n'
    """


    headerRows = '  ' ## adds spaces for formatting purposes
    dashes = generate_dashed_row(width) # gets the second row of dashes

    for w in range(width):
        headerRows += str(w+1)
    headerRows += '\n' + dashes
    
    return headerRows


def display_board(board:list[list[str]]): 

    """
    Displays the board in a readable format
    >>> board = generate_initial_board()
    >>> display_board(board)
          12345678
          --------
        A|++++++++|
        B|++++++++|
        C|++++++++|
        D|+++OX+++|
        E|+++XO+++|
        F|++++++++|
        G|++++++++|
        H|++++++++|
          --------
    """

    header = generate_header_rows(len(board[0])) #gets a header

    footer = generate_dashed_row(len(board[0])) # gets a footer

    print(header) #prints header before the rows

    for rowNum in range(len(board)):
        row = chr(65+rowNum) + '|'
        for colNum in range(len(board[0])):
            row += board[rowNum][colNum]
        row += '|'

        print(row) # prints each row iterably
    
    print(footer) # prints footer after the rows

def get_valid_command(valid_moves: list[str]) -> str:

    """
        Repeatedly asks for inputs until the user gives one that is within a list of valid options. This is not case sensitive but will return caps 
        Only returns the move when a user inputs a valid command
        >>> get_valid_command(["A1","B4"])
        Please enter move (Or H for help): R1
        Please enter move (Or H for help): AAAAA
        Please enter move (Or H for help): 
        Please enter move (Or H for help): b4
        'B4'
    """

    user_input = input("Please enter move (Or H for help): ") # asks user for an input to make a move

    if user_input.upper() == 'H': #help menu
        return 'H'

    elif user_input.upper() == 'Q': # quit game
        return 'Q'
        
    elif user_input.upper() in valid_moves: #returns the valid move to the user formatted to upper case
        return user_input.upper()
    
    else:
        return get_valid_command(valid_moves) #prompts again

def determine_locations(board: list[list[str]], piece: str) -> list[tuple[int,int]]:

    """
        Determines all the locations on the board of the player's piece
        Precondition:
            Only 'X' and 'O' are pieces to be input

        >>> board = generate_initial_board()
        >>> determine_locations(board, 'X')
        [(3, 4), (4, 3)]
    """


    locations_of_pieces = []
    # iterates through the board to determine if any square is the inputted piece
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == piece:
                locations_of_pieces.append((row, column))
    
    return locations_of_pieces

    
    

def get_reversed_positions(board: list[list[str]], piece: str, position: tuple[int,int]) -> list[tuple[int,int]]:

    """
        Determines all the cells that would be flipped to the player's piece if they made a move at a given position

        board = generate_initial_baord()
        >>> get_reversed_positions(board, 'X', (2,3))
        [(3, 3)]
    """

    reversed_positions = []
    other_piece = determine_other_player(piece)
    other_players_pieces = determine_locations(board,other_piece)
    existing_positions = determine_locations(board, piece)
    
    for x in existing_positions:
        line = get_intermediate_locations(x, position) # gets the lines between the inputted position and every piece of the players type
        valid = True
        if line: 
            for y in line:
                if y not in other_players_pieces: # If every item in the line is not the other players pieces ditch the line as it doesnt fit the game rules
                   valid = False
            if valid: # if the line fits the game rules add it to the reversed positions
                for a in range(len(line)):
                    reversed_positions.append(line[a])
        
    return reversed_positions


def get_available_moves(board: list[list[str]], player: str) -> list[str]:

    """
        Returns a list of valid moves a player can make 
        Moves are output as a cellID with a letter (a-z) and a number. 
        >>> board = generate_initial_board()
        >>> get_available_moves(board, "X")
        ['C4', 'D3', 'E6', 'F5']
    """

    available_moves = []
    other_piece = determine_other_player(player)
    current_pieces = determine_locations(board, player)
    other_players_pieces = determine_locations(board, other_piece)
    for x in current_pieces:
        for row in range(len(board)):
            for column in range(len(board[0])): # iterates through the board and gets the reversable lines between every cell and all the players pieces
                reverse = get_reversed_positions(board, player, (row,column)) 
                  # if the line has something in it and fits the game rules add the cell that generated that line to available moves
                for item in reverse:
                    if item in other_players_pieces and (row,column) not in available_moves and not (row,column) in other_players_pieces:
                        available_moves.append((row,column))                
    for move in range(len(available_moves)): # format moves for user
        available_moves[move] = move_to_numeric(available_moves[move])
        
    
    return available_moves

def make_move(board: list[list[str]], piece: str, move: str):

    """
        Places the players piece at the given cell and affects the board accordingly
        Preconditions: 
        - Move is well formed, and given in upper case 
        - Move corresponds to a position that exists on the board 
        - Each row of board will contain the same number of columns

        >>> board = generate_initial_board()
        >>> display_board(board)

          12345678
          --------
        A|++++++++|
        B|++++++++|
        C|++++++++|
        D|+++OX+++|
        E|+++XO+++|
        F|++++++++|
        G|++++++++|
        H|++++++++|
          --------

        >>> make_move(board, "X", "D3")
        >>> display_board(board)

          12345678
          --------
        A|++++++++|
        B|++++++++|
        C|++++++++|
        D|++XXX+++|
        E|+++XO+++|
        F|++++++++|
        G|++++++++|
        H|++++++++|
          --------  
    """

    move_index = move_to_index(move) # change from user format to index
    reversed_indexes = get_reversed_positions(board, piece, move_index) #gets the correct lines to be reveresed
    for coord in range(len(reversed_indexes)): #changes all the cells in the reversed lines to the players piece
        board[reversed_indexes[coord][0]][reversed_indexes[coord][1]] = piece

    board[move_index[0]][move_index[1]] = piece # place a piece where the player moved
    display_board(board)


       
def play_game():

    """
        Plays the game of reversi as per specifications 
        When game is started users an initial game board will be shown and Player 1 'X' will be prompted to have their turn.
        A player should input one of the given moves 
    """

    # initial setup
    print("Welcome to Reversi!")
    board = generate_initial_board()
    display_board(board)

    # Tracks whose turn it is 
    player_turn = 0 
    current_player = 'X'


    game_on = True
    
    while game_on: # loop for while a game is in progress
        # Statements for whos turn it is
        if player_turn%2 == 0:
            current_player = 'X'
            
        else:
            current_player = 'O'
        
        print(f"Player {current_player} to move")

        # List of available moves
        options = get_available_moves(board, current_player)
        available_moves = ""

        # Converts the list to a string

        for index in options:
            if not available_moves == "":
                available_moves += f",{index}"
            else:
                available_moves += index

        # Ends game if a player has no moves
        if available_moves == "": 
            game_on = False
        
        print(f"Available moves: {available_moves}")

        # Gets the input so a player can make a move
        action = get_valid_command(options)

        # Quits game if user inputs q
        if action == 'Q':
            game_on = False
        
        # Displays help message if user inputs h
        elif action =='H':
            print("\n [A-H][1-8]: Make a move at a given cell. \n H/h: Display help message. \n Q/q: End game")
            get_valid_command(options)

        # Makes the move the user inputs
        make_move(board, current_player, action)

        player_turn += 1

    #Game has ended

    print("Game Over!")
    winner = check_winner(board)

    # Prints winner
    if winner == '':
        print("This game resulted in a draw")
    else:
        print(f"{winner} is the winner, you're amazing!")

    # Rematch??? Yes!!
    play_again = input("Would you like to play again? (y/n): ")
    if play_again == 'y':
        play_game()


def main() -> None:
    """
    This function will execute the game and will be initialised on the documents running

    It requires no input and should return no values.
    """
    play_game()


if __name__ == "__main__":
    main()











