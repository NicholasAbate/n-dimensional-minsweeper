#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    visible = []
    board = []
    for r in range(num_rows):
        row = []
        vis_row = []
        for c in range(num_cols):
            neighbors = [(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]
            vis_row.append(False)
            if (r, c) in bombs:         #Unecessary check of [r,c]
                row.append('.')
            else:
                bomb_counter = 0
                for tuple in neighbors:
                    if tuple in bombs:
                        bomb_counter += 1
                row.append(bomb_counter)
        visible.append(vis_row)
        board.append(row)
                                        #Unecessary added for loops, only need one to create base lists
                                        #Deleted crazy helix if checks and replaced it with simple loop over neighbors
    return {
        'dimensions': (num_rows, num_cols),
        'board': board,
        'visible': visible,
        'state': 'ongoing'}


def find_neighbors(game,row,col):
    """
    Helper function to find the neighbors of a square with no nearby bombs. Recursively calls until all 0 neighbor square are found.

    Parameters:
    game(dict) = game board
    row(int) = row value being looked at
    col(int) = col value being looked at
    visible(int) = number of tiles that have already been shown

    Returns:
    int of all the tiles aready shown, updates game['visible'] as well
    """
    visible = 0
    r = row
    c = col
    neighbors = [(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]
    for tuple in neighbors:
        if tuple[0] in range(game['dimensions'][0]) and tuple[1] in range(game['dimensions'][1]):
            if game['board'][tuple[0]][tuple[1]] == 0 and game['visible'][tuple[0]][tuple[1]] != True:
                game['visible'][tuple[0]][tuple[1]] = True
                visible += 1
                visible += find_neighbors(game,tuple[0],tuple[1])
            elif game['visible'][tuple[0]][tuple[1]] != True:
                game['visible'][tuple[0]][tuple[1]] = True
                visible += 1
    return visible

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['visible'][bomb_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    if game['state'] == 'defeat' or game['state'] == 'victory':
        game['state'] = game['state']  # keep the state the same
        return 0

    if game['board'][row][col] == '.':
        game['visible'][row][col] = True
        game['state'] = 'defeat'
        return 1
                                #Unncecessary check if there are uncoverd bombs
                                #No need to check if the game is won here
    if game['visible'][row][col] != True:
        game['visible'][row][col] = True
        revealed = 1
    else:
        return 0

                                #Removed crazy helix if statements
    if game['board'][row][col] == 0:
        revealed += find_neighbors(game,row,col)
    for r in range(game['dimensions'][0]):
        for c in range(game['dimensions'][1]):
            if game['visible'][r][c] == False and game['board'][r][c] != ".":
                return revealed
    game['state'] = "victory"
    return revealed
def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['visible'] indicates which squares should be visible.  If
    xray is True (the default is False), game['visible'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    board = []
    board_row = []
    for j in range(game['dimensions'][0]):
        board_row = []
        for i in range(game['dimensions'][1]):
            if game['visible'][j][i] == True or xray == True:
                if game['board'][j][i] == 0:
                    board_row.append(" ")
                else:
                    board_row.append(str(game['board'][j][i]))
            else:
                board_row.append('_')
        board.append(board_row)
    return board


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    string_imp = ""
    board = render_2d_locations(game,xray)
    for j in range(game['dimensions'][0]):
        string_row = ""
        for i in range(game['dimensions'][1]):
            string_row += board[j][i]
        if j == 0:
            string_imp = string_row
        else:
            string_imp += "\n" + string_row
    return string_imp


# N-D IMPLEMENTATION

def get_val(board,coords):
    """
    Finds the value of a coord in an N-d array.
    Parameters:
    board = N-d array
    coords = valid coordinates (tuple)


    return:
    value at the coordinate fron N-d array

    >>> board = [[1,2],[3,4],[5,6]]
    >>> coords = (1,1)
    >>> get_val(board,coords)
    4
    """
    if len(coords) == 1:
        return board[coords[0]]
    else:
        for i in range(len(board)):
            if i == coords[0]:
                return get_val(board[i],coords[1::])
    return None

def replace_val(board,coords,value):
    """
    Replaces the value in the board at the coordinates with the new value
    Parameters:
    board = N-d array
    coords = valid coordinates (tuple)
    value = new value replacing old value

    Returns:
    None, but change the input board
    >>> board = [[1, 2], [3, 4], [5, 6]]
    >>> coords = (1,1)
    >>> value = 9
    >>> replace_val(board,coords,value)

    """
    if len(coords) == 1:
        board[coords[0]] = value
    else:
        for i in range(len(board)):
            if i == coords[0]:
                replace_val(board[i],coords[1::],value)

def create_same_board(dimensions,value):
    """
    Creates a N-d array with given dimensions where each value is the value given
    Parameters:
    dimensions = list of dimensions for the array
    value = value each point in the array is going to have
    return:
    array with value as its values

    >>> dim = [2,2]
    >>> value = 0
    >>> create_same_board(dim,value)
    [[0, 0], [0, 0]]
    """
    n_list = []
    if len(dimensions) == 1:
        for i in range(dimensions[0]):
            n_list.append(value)
    else:
        for i in range(dimensions[0]):
            n_list.append(create_same_board(dimensions[1::],value))
    return n_list



def get_state(game):
    """
    Returns the state of the game
    Parameters:
    game = a dictionary representing a game

    return:
    string that represents the state of the game
    >>> game = {
    ...    'board': [[1, 2], [".", 4], [5, 6]],
    ...    'dimensions': (3,2),
    ...    'visible': [[True, True], [False, True], [True, True]],
    ...    'state': 'ongoing'
    ...    }

    >>> get_state(game)
    'victory'
    """
    list_board = []
    list_visible = []
    if len(game['dimensions']) == 1:
        cont = False
        for i in range(len(game['board'])):
            if game['board'][i] == "." and game['visible'][i] == True:
                return 'defeat'
            elif game['board'][i] != "." and game['visible'][i] != True:
                cont = True
        if cont:
            return "ongoing"
        else:
            return "victory"
    else:
        new_board = []
        new_visible = []
        for i in range(len(game['board'])):
            new_board +=game['board'][i]
            new_visible += game['visible'][i]
        new_game = {
            'board': new_board,
            'dimensions': game['dimensions'][1::],
            'visible': new_visible,
            'state': game['state'][:]
        }
        return get_state(new_game)


def get_zero_neighbors(game,coord):
    """
    Finds all neighbors, including neighbors of the zeros in neighbors of the original coordinate
    Parameters:
    game = dictionary representation of the game
    coord = tuple representing coordinate of value we are trying to find neighbors of

    Returns:
    list of coordinates representing all neighbors
    """
    neighbors = [coord]
    i = 0
    visited = set()
    while i < len(neighbors):
        if get_val(game['board'],neighbors[i]) == 0 and neighbors[i] not in visited:
            new_neighbors = get_neighbors_coords(game['dimensions'], neighbors[i])
            for new in new_neighbors:
                if new not in neighbors:
                    neighbors.append(new)
        visited.add(neighbors[i])
        i+=1
    return neighbors

def get_neighbors_coords(dim,coord):
    """
    Returns list of neighbor's coordinates
    Parameters:
    dim = tuple of dimensions
    coord = tuple of coordinates for value

    Return:
    list of tuple coords that represent the neighbors
    """
    neighbors = []
    if len(coord) == 1:
        neighbors = [(coord[0]-1,), (coord[0],),(coord[0]+1,)]
        for val in neighbors:
            if val[0] not in range(dim[-1]):
                    neighbors.remove(val)
        return neighbors
    else:
        val = get_neighbors_coords(dim[1:],coord[1:])
        for i in range(coord[0]-1,coord[0]+2):
            for x in val:
                if i in range(dim[0]):
                    neighbors.append((i,)+x)
        return neighbors

def get_neighbors(board,neighbors):
    """
    Returns the neighbors for a given game and coordinates
    Parameters:
    Game = dictionary repsresentation of a game
    coord = tuple coordinates of a value in game

    Return:
    list of neighbors that are near the coord
    """
    neighbor_val = []
    for coordinate in neighbors:
        val = get_val(board,coordinate)
        neighbor_val.append(val)
    return neighbor_val


def find_all_coords(dim):
    """
    Returns a list of all possible coordinates in a dimension.
    Parameters:
    dim = dimensions of a board

    Return:
    list of all coordinates
    """
    coords = []
    if len(dim) == 1:
        for i in range(dim[0]):
            coords.append((i,))
        return coords
    else:
        for i in range(dim[0]):
            lower_d = find_all_coords(dim[1:])
            for coord in lower_d:
                coords.append((i,) + coord)
    return coords







def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    board = create_same_board(dimensions, 0)
    visible = create_same_board(dimensions, False)

    for bomb in bombs:
        replace_val(board,bomb,".")
        neighbors = get_neighbors_coords(dimensions,bomb)
        for neighbor in neighbors:
            if neighbor not in bombs:
                replace_val(board,neighbor,get_val(board,neighbor)+1)
    game = {
        'board': board,
        'visible': visible,
        'dimensions': dimensions[::],
        'state': 'ongoing'
    }
    return game



def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    counter = 0
    if get_val(game['visible'],coordinates) == True:
        return 0
    else:
        replace_val(game['visible'],coordinates,True)
        counter += 1
        game['state'] = get_state(game)
        if game['state'] == 'defeat':
            return counter
        neighbors = get_zero_neighbors(game,coordinates)
        neighbor_vals = get_neighbors(game['board'],neighbors)
        count = 0
        for i in range(len(neighbors)):
            if get_val(game['visible'],neighbors[i]) == False and neighbor_vals[i] != ".":
                replace_val(game['visible'],neighbors[i],True)
                counter += 1

        return counter



def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['visible'] array indicates which squares should be
    visible.  If xray is True (the default is False), the game['visible'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    string_board = create_same_board(game['dimensions'],"_")
    dim = game['dimensions'] [:]
    all_coords = find_all_coords(dim)
    for coord in all_coords:
        if xray == True or get_val(game['visible'],coord) == True:
            val= get_val(game['board'],coord)
            if val == 0:
                val = " "
            replace_val(string_board,coord,str(val))
    return string_board





if __name__ == "__main__":
    #Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
