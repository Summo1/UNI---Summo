# DO NOT modify or add any import statements
from support import *

# Name: Thomas Summerton
# Student Number: 49606782
# Favorite Marsupial: Rock Wallaby
# -----------------------------------------------------------------------------

# Define your functions here (start with def num_hours() -> float)


def num_hours() -> float:
    return 12.4

def move_to_index(cellID:str) -> tuple[int,int]:

    """
        returns the (row, column) index of a coordinate based on a letter (a-z) and numerical input
        >>> move_to_index("A5")
        (0,4)
    """

    rowIndex = ord(cellID[0].upper()) - 65
    columnIndex = int(cellID[1:len(cellID)+1]) - 1

    numericID = (rowIndex, columnIndex)
    return numericID


def move_to_numeric(numericID:tuple[int,int]) -> str:

    """
        returns the alphanumerical cellID of a coordinate based on a (row, column) input
        >>> move_to_index(0,4)
        'A5'
    """

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
    for rowFiller in range(size):
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
    
    counterX = 0
    counterO = 0
    for rowCounter in range(len(board)):
        for item in board[rowCounter]:
            if item == 'X':
                counterX += 1
            elif item == 'O':
                counterO += 1
    if counterX > counterO:
        return 'X'
    elif counterX < counterO:
        return 'O'
    else:
        return ''
                
def get_intermediate_locations(position: tuple[int, int], new_position: tuple[int, int]) -> list[tuple[int, int]]:

    """
        Returns a list of indexes (row, column) that lie within a straight line of two points
        Lines can be vertical, horizontal or, diagonal
        Returns an empty list if the coordinates do not have lines between them or are adjacent coordinates

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

    direction = [0,0]
    
    
    if position == new_position:
        return list_of_locations

    elif position[0] == new_position[0]:
        direction = [0, (new_position[1] - position[1])//abs(new_position[1] - position[1])]
        for x in range(0, new_position[1] - position[1], direction[1]):
            list_of_locations.append((position[0], position[1] + x))
        list_of_locations.remove(list_of_locations[0])
        return list_of_locations

    elif position[1] == new_position[1]:
        direction = [(new_position[0] - position[0])//abs(new_position[0] - position[0]), 0]
        for x in range(0, new_position[0] - position[0], direction[0]):
            list_of_locations.append((position[0] + x, position[1]))
        list_of_locations.remove(list_of_locations[0])
        return list_of_locations

    elif (new_position[0] - position[0])/(new_position[1] - position[1]) == 1 or (new_position[0] - position[0])/(new_position[1] - position[1]) == -1:
        direction = [(new_position[0] - position[0])//abs(new_position[0] - position[0]), (new_position[1] - position[1])//abs(new_position[1] - position[1])]
        
        temp_list = []
        for vert in range(0, new_position[0] - position[0], direction[0]):
            temp_list.append([position[0] + vert])
        for horiz in range(0, new_position[1] - position[1], direction[1]):
            temp_list[horiz].append(position[1] + horiz)
        for a in range(len(temp_list)):
            list_of_locations.append((temp_list[a][0],temp_list[a][1]))

        list_of_locations.remove(list_of_locations[0])
        return list_of_locations
    
    else:
        return list_of_locations

    
def generate_dashed_row(width:int) -> str:

    """
        Generates a dashed row based on the width of a board for displaying a board. 2nd and final rows

        >>> generate_dashed_row(4)
        '  ----\n'
    """


    dashedRow = '  '
    for w in range(width):
        dashedRow += '-'
    dashedRow += '\n'
    
    return dashedRow

def generate_header_rows(width:int) -> str:

    """
    Generates a header row for displaying a board that has the column numbers and a dashed row

    >>> generate_header_rows(4)
    '  1234\n  ----\n'
    """


    headerRows = '  '
    dashes = generate_dashed_row(width)

    for w in range(width):
        headerRows += str(w+1)
    headerRows += '\n' + dashes
    
    return headerRows

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
    
    if piece == "X":
        other_piece = "O"
    elif piece == "O":
        other_piece = "X"
    return other_piece

def display_board(board:list[list[str]]) -> str: 

    """
    prints the inputted board in a visually appealing manner
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

    header = generate_header_rows(len(board[0]))
    footer = generate_dashed_row(len(board[0]))
    displayedBoard = header
    
    for rowNum in range(len(board)):
        displayedBoard = displayedBoard + chr(65+rowNum) + '|'
        for colNum in range(len(board[0])):
                displayedBoard += board[rowNum][colNum]

        displayedBoard += '| \n'
    displayedBoard += footer
        
    return print(displayedBoard)


def get_valid_command(valid_moves: list[str]) -> str:

    """
        Prompts the user until they input a valid command based on a set of valid moves 
        Only returns the move when a user inputs a valid command
        >>> get_valid_command(["A1","B4"])
        Please enter move (Or H for help): R1
        Please enter move (Or H for help): AAAAA
        Please enter move (Or H for help): 
        Please enter move (Or H for help): b4
        'B4'
    """

    user_input = input("Please enter move (Or H for help): ")

    if user_input == 'h' or user_input == 'H':
        print("\n [A-H][1-8]: Please place at specified square. \n H/h: Display help message. \n Q/q: Quit current game.")
        get_valid_command(valid_moves)
        pass

    elif user_input == 'q' or user_input == 'Q':
        return 'end'
        
    elif user_input in valid_moves or user_input.upper() in valid_moves:
        return str(user_input.upper())
    
    else:
        get_valid_command(valid_moves)

def determine_locations(board: list[list[str]], piece: str) -> list[tuple[int,int]]:

    """
        Determines all the locations on the board of a specific piece
        Precondition:
            Only 'X' and 'O' are pieces to be input

        >>> board = generate_initial_board()
        >>> determine_locations(board, 'X')
        [(3, 4), (4, 3)]
    """


    locations_of_pieces = []

    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == piece:
                locations_of_pieces.append((row, column))
    
    return locations_of_pieces

    
    

def get_reversed_positions(board: list[list[str]], piece: str, position: tuple[int,int]) -> list[tuple[int,int]]:

    """
        Determines what indexes (row,column) would be reversed if a player placed a piece at a certain position on a given board

        board = generate_initial_baord()
        >>> get_reversed_positions(board, 'X', (2,3))
        [(3, 3)]
    """

    reversed_positions = []
    other_piece = determine_other_player(piece)
    other_players_pieces = determine_locations(board,other_piece)
    existing_positions = determine_locations(board, piece)
    
    if position in other_players_pieces or position in existing_positions:
        return reversed_positions
    
    for x in existing_positions:
        line = get_intermediate_locations(x, position)
        valid = True
        if line:
            for y in line:
                if y not in other_players_pieces:
                   valid = False
            if valid:
                for a in range(len(line)):
                    reversed_positions.append(line[a])
        
    return reversed_positions


def get_available_moves(board: list[list[str]], player: str) -> list[str]:

    """
        Determines a list of valid moves a player can make according to the game rules
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
            for column in range(len(board[0])):
                reverse = get_reversed_positions(board, player, (row,column))
                if reverse and (row,column) not in available_moves:
                    available_moves.append((row,column))                   
    for move in range(len(available_moves)):
        available_moves[move] = move_to_numeric(available_moves[move])
        
    
    return available_moves

def make_move(board: list[list[str]], piece: str, move: str):

    """
        Places the given piece at the designated position on the board, and updates the game state according to the game rules.
        Preconditions: 
        Move is well formed, and given in upper case 
        Move corresponds to a position that exists on the board 
        Each row of board will contain the same number of columns

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

    move_index = move_to_index(move)

    action_coord = move_to_index(move)
    reversed_indexes = get_reversed_positions(board, piece, action_coord)
    for coord in range(len(reversed_indexes)):
        board[reversed_indexes[coord][0]][reversed_indexes[coord][1]] = piece

    board[move_index[0]][move_index[1]] = piece
    display_board(board)
    return board


    

                
def play_game():

    """
    
    """


    print("Welcome to Reversi! \n")
    board = generate_initial_board()
    display_board(board)
    player_turn = 0
    current_player = 'X'
    game_on = True
    
    while game_on == True:
        if player_turn%2 == 0:
            current_player = 'X'
            print("Player 1 to move")
        else:
            current_player = 'O'
            print("Player 2 to move")
        print(current_player)
        options = get_available_moves(board, current_player)
        available_moves = ""
        for index in options:
            if not available_moves == "":
                available_moves += f",{index}"
            else:
                available_moves += index

        if available_moves == "":
            break
        
        print(f"Possible moves: {available_moves}")

        action = get_valid_command(options)
        if action == 'end':
            break

        make_move(board, current_player, action)
        
        

        
        


        player_turn += 1

    print("Game Over!")
    winner = check_winner(board)
    if winner == '':
        print("Its a draw! Now that is impressive.")
    else:
        print(winner)
    play_again = input("Would you like to play again? (y/n): ")
    if play_again == 'y':
        play_game()

    pass

def main() -> None:
    """
    The main function (You should write a better docstring!)
    play_game()
    """
    play_game()
    
    pass


if __name__ == "__main__":
    main()











